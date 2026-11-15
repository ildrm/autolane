import json
import logging
from functools import wraps
from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, connection
from django.http import JsonResponse, StreamingHttpResponse, FileResponse
from django.middleware.csrf import get_token
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from . import authentication as auth, domain as d, services as s
from .contracts import route_match, validate_input, project_response
from .models import (
    Appointment,
    Auction,
    Audit,
    Bid,
    Branch,
    Inspection,
    Lead,
    Notification,
    Record,
    Slot,
    Taxonomy,
    User,
)
from .permissions import auction_access

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    return JsonResponse(
        {
            "code": "csrf_failed",
            "message": "Your session verification expired. Refresh and try again.",
        },
        status=403,
    )


def boundary(fn):
    @wraps(fn)
    def wrapped(request, *args, **kwargs):
        try:
            if request.body and len(request.body) > 2_000_000:
                raise d.DomainError("request_too_large", "This request is too large.", 413)
            result = fn(request, *args, **kwargs)
            if isinstance(result, (JsonResponse, StreamingHttpResponse, FileResponse)):
                return result
            data, status = result
            response = JsonResponse(data, safe=isinstance(data, dict), status=status)
            if isinstance(data, dict) and data.get("version"):
                response["ETag"] = f'"{data["version"]}"'
            return response
        except d.DomainError as e:
            response = JsonResponse(
                {"code": e.code, "message": e.message, "fields": e.fields}, status=e.status
            )
            if e.status == 429:
                response["Retry-After"] = "300"
            return response
        except (ObjectDoesNotExist, ValueError, TypeError, KeyError):
            return JsonResponse(
                {
                    "code": "invalid_reference",
                    "message": "The requested record or input is not valid.",
                },
                status=404,
            )
        except (ValidationError, json.JSONDecodeError) as e:
            return JsonResponse(
                {
                    "code": "validation_error",
                    "message": "Review your input.",
                    "fields": {"form": str(e)[:200]},
                },
                status=422,
            )
        except IntegrityError:
            return JsonResponse(
                {
                    "code": "conflict",
                    "message": "Another action changed this record. Refresh and try again.",
                },
                status=409,
            )
        except Exception:
            logger.exception("Unhandled request failure: %s", request.path)
            return JsonResponse(
                {
                    "code": "service_error",
                    "message": "We could not complete this request. Try again.",
                },
                status=500,
            )

    return wrapped


def payload(request):
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise d.DomainError("invalid_json", "Send a valid JSON object.", 400)
    d.require(
        isinstance(data, dict),
        "invalid_json",
        "Send a JSON object rather than an array or scalar.",
        400,
    )
    return data


@boundary
def health(request):
    with connection.cursor() as c:
        c.execute("SELECT 1")
    return {
        "status": "ok",
        "environment": settings.APP_ENV,
        "finance_mode": "external_evidence_only",
    }, 200


@ensure_csrf_cookie
@boundary
def register(request):
    d.require(request.method == "POST", "method_not_allowed", "Use POST.", 405)
    return auth.register_user(request, payload(request))


@ensure_csrf_cookie
@boundary
def contract_endpoint(request, route):
    d.require(
        not request.headers.get("Authorization"),
        "unsupported_credential",
        "This build supports browser sessions; the bearer identity adapter is not configured.",
        401,
    )
    extensions = {
        "auth/login": lambda: auth.begin_session(request, payload(request)),
        "auth/verify-email": lambda: auth.verify_email(payload(request)),
        "auth/csrf": lambda: ({"csrf_token": get_token(request)}, 200),
        "auth/action-challenges": lambda: auth.start_stepup(request, payload(request)),
    }
    if route in extensions:
        d.require(
            request.method == ("GET" if route == "auth/csrf" else "POST"),
            "method_not_allowed",
            "Unsupported request method.",
            405,
        )
        return extensions[route]()
    op, params = route_match(route, request.method)
    data = payload(request) if request.method != "GET" else {}
    validate_input(op, data)
    result, status = dispatch(request, op["operationId"], data, params, route)
    return project_response(op, result, status), status


def dispatch(request, op, data, params, route):
    pk = params.get("id", params.get("auctionId"))
    direct = {
        "createSellerLead": d.create_lead,
        "createAppointment": d.book,
        "createInspection": s.create_inspection,
        "createAuction": s.create_auction,
    }
    commands = {
        "transitionAppointment": d.appointment_transition,
        "submitBid": d.bid,
        "closeAuction": d.close,
        "recordSellerDecision": d.seller_decision,
        "createInspectionRevision": d.create_revision,
        "publishInspection": d.publish,
        "transitionSellerLead": s.lead_transition,
        "transitionInspection": s.inspection_transition,
        "transitionAuction": s.auction_transition,
        "approveReconciliation": d.approve_reconciliation,
    }
    if op in direct:
        return direct[op](request, data)
    if op in commands:
        return commands[op](request, data, pk)
    if op == "completeAuthChallenge":
        return auth.complete_challenge(request, data)
    if op == "createStepUpChallenge":
        return auth.start_stepup(request, data)
    if op == "completeStepUp":
        return auth.complete_challenge(request, data, "stepup")
    if op == "readCurrentSession":
        return auth.session_dto(request), 200
    if op == "revokeCurrentSession":
        logout(request)
        return {}, 200
    if op == "requestAccountRecovery":
        return auth.recovery(request, data)
    if op == "completeRecovery":
        return auth.complete_recovery(request, data)
    if op == "listVehicleTaxonomy":
        return {
            "items": [
                {
                    "id": str(t.id),
                    "name": t.name,
                    "kind": t.kind,
                    "parent_id": str(t.parent_id) if t.parent_id else None,
                }
                for t in Taxonomy.objects.order_by("name")
            ],
            "next_cursor": None,
        }, 200
    if op == "listBranches":
        return {
            "items": [
                {
                    "id": str(b.id),
                    "name": b.name,
                    "slug": b.slug,
                    "city": b.city,
                    "address": b.address,
                    "timezone": b.timezone,
                }
                for b in Branch.objects.filter(active=True)
            ],
            "next_cursor": None,
        }, 200
    if op == "listBranchSlots":
        return {
            "items": [
                {
                    "id": str(v.id),
                    "starts_at": v.starts_at.isoformat().replace("+00:00", "Z"),
                    "ends_at": v.ends_at.isoformat().replace("+00:00", "Z"),
                    "timezone": v.branch.timezone,
                    "available": v.reserved < v.capacity,
                }
                for v in Slot.objects.filter(
                    branch_id=pk, starts_at__gt=timezone.now(), branch__active=True
                ).order_by("starts_at")[:100]
            ]
        }, 200
    if op in ["listConsumerListings", "readVehicleListing", "readListingBySlug"]:
        qs = Record.objects.filter(
            kind="VehicleListing", status__in=["available", "unavailable", "sold"]
        ).select_related("vehicle__make", "vehicle__model")
        if op != "listConsumerListings":
            r = qs.get(pk=pk) if pk else qs.get(data__slug=params["slug"])
            return s.listing_dto(r), 200
        qs = qs.filter(status="available", vehicle__channel="")
        for field in ["make_id", "model_id", "transmission"]:
            if value := request.GET.get(field):
                qs = qs.filter(
                    **{
                        (
                            "vehicle__details__transmission"
                            if field == "transmission"
                            else "vehicle__" + field
                        ): value
                    }
                )
        for key, field in [
            ("year_min", "vehicle__year__gte"),
            ("year_max", "vehicle__year__lte"),
            ("price_min_minor", "data__asking_minor__gte"),
            ("price_max_minor", "data__asking_minor__lte"),
        ]:
            if request.GET.get(key):
                if key.startswith("price"):
                    d.require(
                        bool(request.GET.get("currency")),
                        "currency_required",
                        "Select a currency for price filters.",
                        422,
                    )
                qs = qs.filter(**{field: int(request.GET[key])})
        if request.GET.get("currency"):
            qs = qs.filter(data__currency=request.GET["currency"])
        return {
            "items": [s.listing_dto(r) for r in qs.order_by("-created_at", "id")[:100]],
            "next_cursor": None,
        }, 200
    if op == "readPublishedContent":
        r = Record.objects.get(
            kind="Content", status="published", data__content__slug=params["slug"]
        )
        content = r.data["content"]
        return {
            "slug": content["slug"],
            "title": content["title"],
            "blocks": content["blocks"],
            "canonical_path": content["canonical_path"],
            "published_at": r.data["published_at"],
            "reviewed_at": r.data["published_at"],
            "author_display_name": r.owner.get_full_name() or "Autolane editorial",
        }, 200
    if op == "estimatePublicVehicle":
        return {
            "status": "insufficient_data",
            "policy_version": "unconfigured",
            "as_of": timezone.now().isoformat().replace("+00:00", "Z"),
            "disclaimer": "A licensed market data source is not configured. Book an inspection for an individual review.",
        }, 200
    if op == "getMetrics":
        d.role(request.user, "ROLE-017")
        return {
            "as_of": timezone.now().isoformat().replace("+00:00", "Z"),
            "metrics": {
                "leads": Lead.objects.count(),
                "appointments": Appointment.objects.count(),
                "published_inspections": Inspection.objects.filter(status="published").count(),
                "active_auctions": Auction.objects.filter(status="open").count(),
                "accepted_bids": Bid.objects.count(),
            },
        }, 200
    if op in ["readBidCommand", "listBidCommand"]:
        d.eligible_member(request.user)
        qs = Bid.objects.filter(membership__user=request.user)

        def bd(b):
            return {
                "id": str(b.id),
                "version": 1,
                "auction_id": str(b.auction_id),
                "status": "accepted",
                "amount_minor": b.amount_minor,
                "currency": b.auction.currency,
                "sequence": b.sequence,
                "accepted_at": b.accepted_at.isoformat().replace("+00:00", "Z"),
            }

        return (
            bd(qs.get(pk=pk))
            if pk
            else {"items": [bd(b) for b in qs.order_by("-created_at")[:100]], "next_cursor": None}
        ), 200
    if op.startswith("transition") and route.split("/")[0] in s.RECORD_KINDS:
        return s.record_transition(request, data, pk)
    creators = {
        "createVehicleListing": "VehicleListing",
        "createValuation": "Valuation",
        "createPurchaseRequest": "PurchaseRequest",
        "createContract": "Contract",
        "createDelivery": "Delivery",
        "createWarrantyClaim": "WarrantyClaim",
        "createSupportTicket": "SupportTicket",
        "createFinancingApplication": "FinancingApplication",
        "createProcurement": "ProcurementRequest",
        "createPrivacyRequest": "PrivacyRequest",
        "createContent": "Content",
        "createCampaign": "Campaign",
    }
    if op in creators:
        return s.create_record(request, data, creators[op])
    if op in ["createUploadGrant", "createDownloadGrant"]:
        from .files import create_grant, download_grant

        return (create_grant if op == "createUploadGrant" else download_grant)(
            request, data, *([pk] if pk else [])
        )
    if op in ["requestExport", "downloadExport"]:
        from .exports import request_export, grant

        return request_export(request, data) if op == "requestExport" else grant(request, data, pk)
    if op in [
        "readPreferences",
        "changePreference",
        "listSavedVehicles",
        "setSavedVehicle",
        "createSavedSearch",
        "listSavedSearches",
        "deleteSavedSearch",
    ]:
        from .operations import account_operation

        return account_operation(request, op, data, pk)
    from .operations import OPERATIONS

    if op in OPERATIONS:
        return OPERATIONS[op](request, data, pk)
    if request.method == "GET":
        base = route.rsplit("/", 1)[0] if pk else route
        if base in s.MODEL_KINDS or base in s.RECORD_KINDS:
            if pk:
                obj = s.resource(base, pk)
                s.access(request.user, obj)
                return s.dto(obj), 200
            items = s.visible(request.user, base).order_by("-created_at", "id")
            size = min(max(int(request.GET.get("limit", 25)), 1), 100)
            return {"items": [s.dto(i) for i in items[:size]], "next_cursor": None}, 200
    raise d.DomainError(
        "not_implemented", "This operation is not implemented in the current build.", 501
    )


@boundary
def workspace(request, kind=None, pk=None):
    d.require(request.user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    if not kind:
        return {
            "user": {
                "id": str(request.user.id),
                "name": request.user.get_full_name(),
                "email": request.user.email,
                "roles": request.user.roles,
            },
            "environment": settings.APP_ENV,
            "notifications": [
                {"id": str(n.id), "subject": n.subject, "body": n.body}
                for n in Notification.objects.filter(recipient=request.user).order_by(
                    "-created_at"
                )[:20]
            ],
        }, 200
    if kind == "audit":
        d.role(request.user, "ROLE-016")
        return {
            "items": [
                {
                    "id": a.id,
                    "action": a.action,
                    "object_type": a.object_type,
                    "object_id": a.object_id,
                    "occurred_at": a.occurred_at.isoformat(),
                }
                for a in Audit.objects.order_by("-id")[:100]
            ]
        }, 200
    if kind == "users":
        d.role(request.user, "ROLE-016")
        return {
            "items": [
                {
                    "id": str(u.id),
                    "name": u.get_full_name(),
                    "roles": u.roles,
                    "active": u.is_active,
                }
                for u in User.objects.order_by("username")[:100]
            ]
        }, 200
    d.require(
        request.method == "GET", "method_not_allowed", "Use the documented domain commands.", 405
    )
    return {
        "items": [s.dto(i) for i in s.visible(request.user, kind).order_by("-created_at")[:100]]
    }, 200


@boundary
def auction_events(request, pk):
    a = Auction.objects.get(pk=pk)
    auction_access(request.user, a)
    # One-shot SSE snapshot: clients reconnect to reauthorize and never hold a worker indefinitely.
    body = (
        "id: "
        + str(a.sequence)
        + "\nevent: snapshot\ndata: "
        + json.dumps(d.auction_dto(a))
        + "\n\n"
    )
    response = StreamingHttpResponse(iter([body]), content_type="text/event-stream")
    response["Cache-Control"] = "private, no-store"
    return response


def file_upload(request, pk):
    from .files import upload

    try:
        data, status = upload(request, pk)
        return JsonResponse(data, status=status)
    except d.DomainError as e:
        return JsonResponse({"code": e.code, "message": e.message}, status=e.status)
    except (ObjectDoesNotExist, ValueError):
        return JsonResponse({"code": "not_found", "message": "Upload not available."}, status=404)


@boundary
def file_download(request, pk):
    from .files import download

    return download(request, pk)


@boundary
def export_download(request, pk):
    from .exports import download

    return download(request, pk)
