from .models import Membership
import hashlib
import json
import re
from datetime import timedelta
from uuid import uuid4
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from . import domain as d
from .contracts import MACHINES
from .models import (
    Appointment,
    Auction,
    Inspection,
    Lead,
    Obligation,
    Organization,
    Record,
    Result,
    Revision,
    TransactionCase,
    User,
    Vehicle,
)
from .permissions import DOMAIN_ROLES, auction_access, case_access, lead_access, record_access

MODEL_KINDS = {
    "seller-leads": Lead,
    "appointments": Appointment,
    "inspections": Inspection,
    "auctions": Auction,
    "auction-results": Result,
    "transactions": TransactionCase,
    "obligations": Obligation,
    "inspection-revisions": Revision,
}
RECORD_KINDS = {
    "consumer-offers": "ConsumerOffer",
    "listings": "VehicleListing",
    "inventory/listings": "VehicleListing",
    "valuations": "Valuation",
    "dealer-verifications": "DealerVerification",
    "purchase-requests": "PurchaseRequest",
    "financing-applications": "FinancingApplication",
    "contracts": "Contract",
    "deliveries": "Delivery",
    "claims": "WarrantyClaim",
    "support-tickets": "SupportTicket",
    "ownership-transfers": "OwnershipTransfer",
    "reconciliations": "Reconciliation",
    "admin/policies": "Policy",
    "procurement-requests": "ProcurementRequest",
    "privacy-requests": "PrivacyRequest",
    "content-items": "Content",
    "campaigns": "Campaign",
    "inspection-templates": "InspectionTemplate",
    "files": "File",
    "exports": "Export",
}


def authorize_object(user, pk):
    for model in [
        Lead,
        Appointment,
        Inspection,
        Auction,
        Result,
        TransactionCase,
        Obligation,
        Revision,
        Record,
    ]:
        obj = model.objects.filter(pk=pk).first()
        if obj:
            access(user, obj)
            return
    raise d.DomainError("not_found", "This record is not available.", 404)


def access(user, obj):
    d.require(user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    if isinstance(obj, Lead):
        lead_access(user, obj)
    elif isinstance(obj, Appointment):
        lead_access(user, obj.lead)
    elif isinstance(obj, Inspection):
        if obj.vehicle.owner_id == user.id:
            return
        d.role(user, "ROLE-007", "ROLE-008")
        d.branch_scope(user, obj.branch_id)
        if "ROLE-008" not in user.roles:
            d.own(user, obj.inspector_id)
    elif isinstance(obj, Revision):
        if "ROLE-004" in user.roles:
            auctions = Auction.objects.filter(
                report=obj, status__in=["scheduled", "open", "paused", "closed"]
            )
            d.require(
                obj.status == "published" and auctions.exists(),
                "not_found",
                "Report unavailable.",
                404,
            )
            d.eligible_member(user)
        else:
            access(user, obj.inspection)
            if obj.inspection.vehicle.owner_id == user.id:
                d.require(obj.status == "published", "not_found", "Report unavailable.", 404)
    elif isinstance(obj, Auction):
        auction_access(user, obj)
    elif isinstance(obj, Result):
        auction_access(user, obj.auction)
    elif isinstance(obj, TransactionCase):
        case_access(user, obj)
    elif isinstance(obj, Obligation):
        case_access(user, obj.transaction)
    else:
        record_access(user, obj)


def record_dto(r):
    base = {"id": str(r.id), "version": r.version, "status": r.status}
    if r.kind == "Reconciliation":
        base.update(
            status={"prepared": "pending_review", "approved": "reconciled"}.get(r.status, r.status),
            prepared_by=str(r.prepared_by_id),
        )
    if r.kind == "Policy":
        base["policy_version_id"] = str(r.id)
    safe = {
        k: v
        for k, v in r.data.items()
        if k not in ["storage_path", "grant_hash", "review_notes", "secret", "assigned_to"]
    }
    if r.kind == "Content":
        return {**base, "revision_id": r.data["revision_id"], "content": r.data["content"]}
    if r.kind == "Campaign":
        return {**base, "definition": {k: v for k, v in r.data.items() if k != "last_reason"}}
    if r.kind == "ProcurementRequest":
        return {
            **base,
            "criteria": r.data.get("criteria_snapshot", r.data),
            **({"advisor_id": r.data["advisor_id"]} if r.data.get("advisor_id") else {}),
        }
    if r.kind == "InspectionTemplate":
        return {**base, "jurisdiction": r.data["jurisdiction"], "points": r.data["points"]}
    return {**safe, **base}


def listing_dto(r):
    v = r.vehicle
    return {
        "id": str(r.id),
        "title": r.data["title"],
        "price_minor": r.data["asking_minor"],
        "currency": r.data["currency"],
        "status": r.status,
        "slug": r.data["slug"],
        "revision": r.version,
        "vehicle": d.public_vehicle(v),
        "media": v.details.get("media", []),
        "region_name": r.data.get("region_name", "Not specified"),
        "condition_summary": r.data.get(
            "condition_summary", "Request the published inspection summary."
        ),
        "published_at": r.data.get("published_at", r.created_at.isoformat().replace("+00:00", "Z")),
    }


def dto(obj):
    if isinstance(obj, Lead):
        return {"id": str(obj.id), "status": obj.status, "version": obj.version}
    if isinstance(obj, Appointment):
        return d.appointment_dto(obj)
    if isinstance(obj, Auction):
        return d.auction_dto(obj)
    if isinstance(obj, Result):
        return d.result_dto(obj)
    if isinstance(obj, Revision):
        return d.revision_dto(obj)
    if isinstance(obj, Inspection):
        r = obj.revision_set.order_by("-number").first()
        return {
            "id": str(obj.id),
            "version": obj.version,
            "status": obj.status,
            "vehicle_id": str(obj.vehicle_id),
            "branch_id": str(obj.branch_id),
            "inspector_id": str(obj.inspector_id),
            "template_version_id": str(obj.template_id),
            **({"current_revision_id": str(r.id)} if r else {}),
        }
    if isinstance(obj, TransactionCase):
        result = {"id": str(obj.id), "version": obj.version, "status": obj.status}
        for kind, field in [
            ("Contract", "contract_id"),
            ("Delivery", "delivery_id"),
            ("OwnershipTransfer", "transfer_id"),
        ]:
            r = Record.objects.filter(kind=kind, data__transaction_id=str(obj.id)).first()
            if r:
                result[field] = str(r.id)
        ids = [str(o.id) for o in obj.obligation_set.all()]
        if ids:
            result["obligation_ids"] = ids
        return result
    if isinstance(obj, Obligation):
        return {
            "id": str(obj.id),
            "version": obj.version,
            "status": obj.status,
            "transaction_id": str(obj.transaction_id),
            "amount_minor": obj.amount_minor,
            "currency": obj.currency,
        }
    return record_dto(obj)


def resource(route, pk):
    if route in MODEL_KINDS:
        return MODEL_KINDS[route].objects.get(pk=pk)
    return Record.objects.get(pk=pk, kind=RECORD_KINDS[route])


def visible(user, kind):
    d.require(user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    if kind == "seller-leads":
        return Lead.objects.filter(Q(owner=user) | Q(assigned_to=user)).distinct()
    if kind == "appointments":
        return Appointment.objects.filter(
            Q(lead__owner=user) | Q(slot__branch__employees=user)
        ).distinct()
    if kind == "inspections":
        q = Inspection.objects.filter(Q(vehicle__owner=user) | Q(inspector=user))
        if "ROLE-008" in user.roles:
            q = Inspection.objects.filter(Q(vehicle__owner=user) | Q(branch__employees=user))
        return q.distinct()
    if kind == "auctions":
        if "ROLE-004" in user.roles:
            d.eligible_member(user)
            return Auction.objects.filter(status__in=["scheduled", "open", "paused", "closed"])
        if "ROLE-010" in user.roles:
            return Auction.objects.filter(report__inspection__branch__employees=user).distinct()
        return Auction.objects.filter(vehicle__owner=user)
    if kind == "obligations":
        q = Q(transaction__seller=user) | Q(transaction__buyer=user)
        if set(user.roles) & {"ROLE-013", "ROLE-014"}:
            q |= Q(transaction__branch__employees=user)
        return Obligation.objects.filter(q).distinct()
    if kind == "transactions":
        return TransactionCase.objects.filter(Q(seller=user) | Q(buyer=user)).distinct()
    rkind = RECORD_KINDS.get(kind)
    qs = Record.objects.filter(kind=rkind)
    roles = DOMAIN_ROLES.get(rkind, [])
    if set(user.roles) & set(roles):
        if rkind in [
            "Content",
            "Campaign",
            "Policy",
            "InspectionTemplate",
            "DealerVerification",
            "PrivacyRequest",
        ]:
            return qs
        return qs.filter(
            Q(owner=user)
            | Q(branch__employees=user)
            | Q(prepared_by=user)
            | Q(data__assigned_to=str(user.id))
        ).distinct()
    return qs.filter(owner=user)


@d.command("createInspection")
def create_inspection(request, data):
    d.role(request.user, "ROLE-006", "ROLE-008")
    d.branch_scope(request.user, data["branch_id"])
    inspector = User.objects.get(pk=data["inspector_id"], is_active=True)
    d.require(
        "ROLE-007" in inspector.roles and inspector.branches.filter(pk=data["branch_id"]).exists(),
        "invalid_inspector",
        "Assign an active inspector in this branch.",
        422,
    )
    d.require(
        Appointment.objects.filter(
            lead__vehicle_id=data["vehicle_id"],
            slot__branch_id=data["branch_id"],
            status="checked_in",
        ).exists(),
        "check_in_required",
        "Check in the vehicle before starting inspection.",
    )
    template = Record.objects.get(
        pk=data["template_version_id"], kind="InspectionTemplate", status="approved"
    )
    i = Inspection.objects.create(
        vehicle_id=data["vehicle_id"],
        branch_id=data["branch_id"],
        inspector=inspector,
        template=template,
    )
    d.emit(request.user, "inspection.created", i, [inspector.id])
    return dto(i), 201


@d.command("createAuction")
def create_auction(request, data):
    d.role(request.user, "ROLE-010")
    v = Vehicle.objects.select_for_update().get(pk=data["vehicle_id"])
    report = Revision.objects.get(
        pk=data["report_revision_id"], inspection__vehicle=v, status="published"
    )
    d.branch_scope(request.user, report.inspection.branch_id)
    policy = Record.objects.get(pk=data["policy_version_id"], kind="Policy", status="approved")
    p = policy.data["content"]
    d.require(
        not v.channel or v.channel == "auction",
        "channel_conflict",
        "This vehicle is committed to another sale channel.",
    )
    d.require(
        not Auction.objects.filter(
            vehicle=v, status__in=["draft", "scheduled", "open", "paused"]
        ).exists(),
        "auction_exists",
        "This vehicle already has an active auction.",
    )
    start, end = parse_datetime(data["starts_at"]), parse_datetime(data["closes_at"])
    d.require(
        start < end and end > d.db_now(),
        "invalid_deadline",
        "Choose a future closing time after the start.",
        422,
    )
    d.require(
        p.get("currency") == data["currency"],
        "currency_mismatch",
        "Use the pinned policy currency.",
        422,
    )
    a = Auction.objects.create(
        vehicle=v,
        report=report,
        policy=policy,
        starts_at=start,
        closes_at=end,
        currency=data["currency"],
        starting_minor=d.money(p["starting_minor"]),
        increment_minor=d.money(p["increment_minor"]),
        reserve_minor=p.get("reserve_minor"),
        offer_expires_at=end + timedelta(hours=p.get("seller_response_hours", 24)),
    )
    v.channel = "auction"
    v.save()
    d.emit(request.user, "auction.created", a)
    return dto(a), 201


@d.command("transitionSellerLead")
def lead_transition(request, data, pk):
    lead = Lead.objects.select_for_update().get(pk=pk)
    lead_access(request.user, lead)
    d.version(request, lead)
    t = transition_rule("SellerLead", lead.status, data["action"], request.user)
    if data["action"] == "submit":
        d.own(request.user, lead.owner_id)
        d.require(
            request.user.contact_verified, "contact_unverified", "Verify your contact first.", 403
        )
    elif data["action"] == "qualify":
        d.require(
            bool(data.get("evidence_ids")),
            "evidence_required",
            "Record checked seller authority evidence.",
            422,
        )
        for fid in data["evidence_ids"]:
            d.clean_evidence(request.user, fid)
    elif data["action"] == "start-case":
        d.require(
            Appointment.objects.filter(lead=lead, status__in=["confirmed", "checked_in"]).exists(),
            "booking_required",
            "A confirmed visit is required.",
        )
    elif data["action"] in ["cancel", "close"]:
        d.require(
            not TransactionCase.objects.filter(
                vehicle=lead.vehicle, status__in=["open", "on_hold"]
            ).exists(),
            "obligation_open",
            "Resolve the open transaction first.",
        )
        d.require(
            not Appointment.objects.filter(
                lead=lead, status__in=["confirmed", "checked_in"]
            ).exists(),
            "appointment_open",
            "Cancel or complete the active appointment first.",
        )
    lead.status, lead.version = t["destination"], lead.version + 1
    lead.save()
    d.emit(request.user, "seller.lead_" + data["action"], lead, [lead.owner_id])
    return dto(lead), 200


def transition_rule(entity, state, action, user):
    matches = [
        t
        for t in MACHINES[entity]["transitions"]
        if action == t["action"] and state in t["source_states"]
    ]
    d.require(
        len(matches) == 1, "invalid_transition", "This action is not allowed in the current state."
    )
    t = matches[0]
    roles = re.findall(r"ROLE-\d+", t["actor"])
    d.require(
        bool(roles),
        "provider_action_required",
        "This action requires authenticated provider evidence.",
        403,
    )
    d.role(user, *roles)
    return t


@d.command("transitionInspection")
def inspection_transition(request, data, pk):
    if data["action"] == "publish":
        return d.publish.__wrapped__(request, data, pk)
    i = Inspection.objects.select_for_update().get(pk=pk)
    access(request.user, i)
    d.version(request, i)
    t = transition_rule("Inspection", i.status, data["action"], request.user)
    r = Revision.objects.filter(inspection=i).order_by("-number").first()
    d.require(r is not None, "revision_required", "Create a checklist revision first.")
    if data["action"] == "submit":
        d.own(request.user, i.inspector_id)
        d.require(
            str(r.id) == data["revision_id"], "stale_revision", "Review the latest report revision."
        )
        d.complete_findings(i.template, r.findings)
        r.status = "submitted"
        r.save()
    elif data["action"] == "return":
        d.require(
            r.author_id != request.user.id,
            "independent_review_required",
            "Independent review is required.",
            403,
        )
        r.status = "returned"
        r.save()
    elif data["action"] == "correct":
        for a in (
            Auction.objects.select_for_update()
            .filter(report__inspection=i, status__in=["scheduled", "open", "paused"])
            .order_by("id")
        ):
            a.safety_hold = True
            if a.status == "open":
                a.status = "paused"
            a.version += 1
            a.save()
            d.emit(request.user, "auction.safety_hold", a)
    i.status, i.version = t["destination"], i.version + 1
    i.save()
    d.emit(request.user, "inspection." + data["action"], i, [i.vehicle.owner_id])
    return dto(i), 200


@d.command("transitionAuction")
def auction_transition(request, data, pk):
    a = Auction.objects.select_for_update().get(pk=pk)
    d.role(request.user, "ROLE-010")
    d.branch_scope(request.user, a.report.inspection.branch_id)
    d.version(request, a)
    t = transition_rule("Auction", a.status, data["action"], request.user)
    now = d.db_now()
    if data["action"] in ["open", "resume"]:
        d.require(
            a.starts_at <= now < a.closes_at and not a.safety_hold,
            "auction_unavailable",
            "Timing or safety restrictions prevent opening.",
        )
    if data["action"] == "schedule":
        d.require(
            a.report.status == "published" and a.policy.status == "approved",
            "not_approved",
            "Approved report and policy are required.",
        )
    if data["action"] == "close":
        d.close_locked(request.user, a)
        return dto(a), 200
    a.status, a.version = t["destination"], a.version + 1
    a.save()
    d.emit(request.user, "auction." + data["action"], a, [a.vehicle.owner_id])
    return dto(a), 200


@d.command("createOperationalRecord")
def create_record(request, data, kind):
    owner = request.user
    branch = None
    vehicle = None
    org = None
    state = MACHINES.get(kind, {}).get("initial_state", "draft")
    if kind == "ProcurementRequest":
        state = "submitted"
    if kind == "PrivacyRequest":
        state = "received"
    if kind in [
        "SupportTicket",
        "WarrantyClaim",
        "PurchaseRequest",
        "ProcurementRequest",
        "PrivacyRequest",
        "FinancingApplication",
    ]:
        d.role(owner, "ROLE-002", "ROLE-003", "ROLE-004", "ROLE-011")
        if kind == "PurchaseRequest":
            listing = Record.objects.select_for_update().get(
                pk=data["listing_id"], kind="VehicleListing"
            )
            d.require(
                listing.status == "available" and not listing.vehicle.channel,
                "listing_unavailable",
                "This vehicle is unavailable.",
            )
            vehicle = listing.vehicle
        if data.get("transaction_id") or data.get("case_id"):
            case = TransactionCase.objects.get(pk=data.get("transaction_id", data.get("case_id")))
            case_access(owner, case)
            appt = Appointment.objects.filter(lead__vehicle=case.vehicle).first()
            branch = case.branch or (appt.slot.branch if appt else None)
    else:
        d.role(owner, *DOMAIN_ROLES.get(kind, []))
    if data.get("vehicle_id"):
        vehicle = Vehicle.objects.get(pk=data["vehicle_id"])
        appt = Appointment.objects.filter(lead__vehicle=vehicle).first()
        d.require(
            appt is not None, "branch_required", "Assign a vehicle visit before this operation."
        )
        branch = appt.slot.branch
        d.branch_scope(owner, branch.id)
    if kind in ["Contract", "Delivery"]:
        case = TransactionCase.objects.get(pk=data["transaction_id"])
        case_access(owner, case)
        appt = Appointment.objects.filter(lead__vehicle=case.vehicle).first()
        branch = case.branch or (appt.slot.branch if appt else None)
        d.require(
            branch is not None, "branch_required", "The transaction needs an assigned branch."
        )
        d.branch_scope(owner, branch.id)
        if kind == "Contract":
            template = Record.objects.get(
                pk=data["template_version_id"], kind="ContractTemplate", status="approved"
            )
            parties = {str(case.seller_id), str(case.buyer_id)}
            d.require(
                set(data["required_signer_ids"]) == parties,
                "signer_mismatch",
                "Both transaction parties must be required signers.",
                422,
            )
            data.update(
                document_version_id=str(uuid4()),
                template_snapshot=template.data,
                signatures=[],
                document_checksum=hashlib.sha256(
                    json.dumps({**data, "parties": sorted(parties)}, sort_keys=True).encode()
                ).hexdigest(),
            )
    if kind == "Content":
        data = {"content": data, "revision_id": str(uuid4())}
    if kind in [
        "SupportTicket",
        "PurchaseRequest",
        "ProcurementRequest",
        "WarrantyClaim",
        "PrivacyRequest",
    ]:
        target_role = {"WarrantyClaim": "ROLE-022", "PrivacyRequest": "ROLE-023"}.get(
            kind, "ROLE-011"
        )
        advisor = (
            User.objects.filter(is_active=True, roles__contains=[target_role])
            .order_by("date_joined")
            .first()
        )
        if kind == "ProcurementRequest":
            data = {**data, "criteria_snapshot": dict(data)}
        if advisor:
            data["assigned_to"] = str(advisor.id)
    if kind == "Valuation":
        d.require(
            Revision.objects.filter(inspection__vehicle=vehicle, status="published").exists(),
            "report_required",
            "Publish an inspection first.",
        )
    if kind == "VehicleListing":
        d.require(
            not vehicle.channel,
            "channel_conflict",
            "This vehicle is committed to another sale channel.",
        )
        data.setdefault("title", f"{vehicle.year} {vehicle.make.name} {vehicle.model.name}")
        data.setdefault(
            "slug",
            f"{vehicle.year}-{vehicle.make.name.lower()}-{vehicle.model.name.lower()}-{str(vehicle.id)[:8]}",
        )
        data["asking_minor"] = d.money(data["price_minor"])
    if kind == "FinancingApplication":
        raise d.DomainError(
            "provider_not_configured",
            "A financing provider is not configured for this installation.",
            503,
        )
    for fid in data.get("evidence_ids", []):
        d.clean_evidence(owner, fid)
    record = Record.objects.create(
        kind=kind,
        status=state,
        owner=owner,
        prepared_by=owner,
        branch=branch,
        organization=org,
        vehicle=vehicle,
        data=data,
    )
    d.emit(owner, kind.lower() + ".created", record, [owner.id])
    return dto(record), 201


@d.command("transitionOperationalRecord")
def record_transition(request, data, pk):
    r = Record.objects.select_for_update().get(pk=pk)
    record_access(request.user, r)
    d.version(request, r)
    t = transition_rule(r.kind, r.status, data["action"], request.user)
    action = data["action"]
    if r.kind == "DealerVerification":
        org = Organization.objects.select_for_update().get(pk=r.organization_id)
        if action == "resubmit":
            d.require(
                Membership.objects.filter(
                    user=request.user, organization=org, active=True
                ).exists(),
                "access_denied",
                "Only a current organization representative may resubmit.",
                403,
            )
            d.require(
                bool(data.get("evidence_ids")),
                "evidence_required",
                "Attach the requested verification evidence.",
                422,
            )
            r.data["evidence_ids"] = data["evidence_ids"]
        else:
            d.require(
                r.owner_id != request.user.id and r.prepared_by_id != request.user.id,
                "independent_review_required",
                "Review must be independent of the applicant.",
                403,
            )
        if action in ["approve", "reinstate"]:
            d.require(
                bool(r.data.get("evidence_ids")),
                "evidence_required",
                "Verification evidence is required.",
            )
            for fid in r.data["evidence_ids"]:
                d.clean_evidence(request.user, fid)
            org.status = "active"
        elif action in ["reject", "suspend"]:
            if action == "suspend":
                d.fresh(request, "dealer_risk")
            org.status = "suspended" if action == "suspend" else "rejected"
        org.save()
    elif r.kind == "VehicleListing":
        record_access(request.user, r, write=True)
        v = Vehicle.objects.select_for_update().get(pk=r.vehicle_id)
        d.require(
            not v.channel, "channel_conflict", "This vehicle has an exclusive sale commitment."
        )
        if action == "publish":
            d.money(r.data["asking_minor"])
            r.data["published_at"] = timezone.now().isoformat().replace("+00:00", "Z")
    elif r.kind == "Valuation":
        if action == "approve":
            d.require(
                r.prepared_by_id != request.user.id,
                "independent_review_required",
                "An independent pricing reviewer is required.",
                403,
            )
            low, high = (
                d.money(data.get("low_minor", r.data.get("low_minor"))),
                d.money(data.get("high_minor", r.data.get("high_minor"))),
            )
            d.require(
                low <= high, "invalid_range", "The lower value cannot exceed the upper value.", 422
            )
            r.data.update(
                low_minor=low,
                high_minor=high,
                currency=data.get("currency", r.data.get("currency")),
            )
    elif r.kind == "Contract":
        if action in ["record-signature", "complete-signatures"]:
            raise d.DomainError(
                "signature_evidence_required", "Use the verified signature evidence workflow.", 409
            )
        if action == "review":
            d.require(
                r.prepared_by_id != request.user.id,
                "independent_review_required",
                "Independent legal review is required.",
                403,
            )
    elif r.kind == "Delivery":
        if action in ["collect", "deliver"]:
            raise d.DomainError(
                "handover_evidence_required",
                "Record verified handover evidence before this transition.",
                409,
            )
    elif r.kind == "WarrantyClaim":
        if action in ["approve", "deny", "complete-remedy"]:
            d.require(
                bool(data.get("evidence_ids")),
                "evidence_required",
                "Provide decision or remedy evidence.",
                422,
            )
    elif r.kind == "PurchaseRequest":
        if action == "coordinate":
            d.require(
                bool(r.data.get("transaction_id")),
                "accepted_offer_required",
                "A buyer-accepted offer must create the transaction first.",
            )
    elif r.kind != "SupportTicket":
        raise d.DomainError(
            "guard_not_implemented", "This workflow guard is not implemented yet.", 501
        )
    for fid in data.get("evidence_ids", []):
        d.clean_evidence(request.user, fid)
    r.status, r.version, r.reviewed_by = t["destination"], r.version + 1, request.user
    r.data["last_reason"] = data["reason"]
    r.save()
    d.emit(request.user, r.kind.lower() + "." + action, r, [r.owner_id])
    return dto(r), 200
