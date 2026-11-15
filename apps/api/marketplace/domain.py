"""Transactional command boundary. No network calls occur under domain locks."""

import hashlib
import json
from datetime import timedelta
from functools import wraps
from django.db import connection, transaction
from django.utils import timezone
from .models import (
    Appointment,
    Auction,
    Audit,
    Bid,
    CommandReceipt,
    Inspection,
    Lead,
    Membership,
    Obligation,
    Organization,
    Outbox,
    PaymentEvidence,
    Record,
    Result,
    Revision,
    Slot,
    Taxonomy,
    TransactionCase,
    User,
    Vehicle,
)

SAFE_MONEY = 9007199254740991


class DomainError(Exception):
    def __init__(self, code, message, status=409, fields=None):
        self.code, self.message, self.status, self.fields = code, message, status, fields or {}


def require(condition, code, message, status=409):
    if not condition:
        raise DomainError(code, message, status)


def role(user, *roles):
    require(
        user.is_authenticated and user.is_active,
        "authentication_required",
        "Sign in to continue.",
        401,
    )
    require(
        bool(set(user.roles) & set(roles)),
        "access_denied",
        "You do not have permission for this action.",
        403,
    )


def branch_scope(user, branch_id):
    require(
        user.branches.filter(id=branch_id).exists(),
        "access_denied",
        "This branch is outside your assignment.",
        403,
    )


def own(user, owner_id):
    require(str(user.id) == str(owner_id), "not_found", "This record is not available.", 404)


def fresh(request, purpose):
    grant = request.session.get("step_up", {})
    require(
        grant.get("purpose") == purpose and grant.get("expires", 0) > timezone.now().timestamp(),
        "step_up_required",
        "Verify your identity to confirm this action.",
        403,
    )


def version(request, entity):
    require(
        request.headers.get("If-Match") == f'"{entity.version}"',
        "stale_version",
        "This record changed. Review the latest version.",
        412,
    )


def money(value):
    require(
        type(value) is int and 0 < value <= SAFE_MONEY,
        "invalid_amount",
        "Enter a positive amount in minor units.",
        422,
    )
    return value


def db_now():
    with connection.cursor() as cursor:
        cursor.execute("SELECT clock_timestamp()")
        return cursor.fetchone()[0]


def audit(user, action, entity, metadata=None):
    Audit.objects.create(
        actor=user,
        action=action,
        object_type=type(entity).__name__,
        object_id=str(entity.pk),
        metadata=metadata or {},
    )


def emit(user, action, entity, recipients=()):
    audit(user, action, entity)
    Outbox.objects.create(
        event_type=action,
        aggregate_id=entity.pk,
        aggregate_version=entity.version,
        available_at=timezone.now(),
        payload={
            "recipients": [str(v) for v in recipients],
            "status": getattr(entity, "status", ""),
        },
    )


def command(operation):
    """Serialize same intent before aggregate locks; rollback any failed mutation."""

    def decorate(fn):
        @wraps(fn)
        def execute(request, payload, *args, **kwargs):
            require(
                request.user.is_authenticated,
                "authentication_required",
                "Sign in to continue.",
                401,
            )
            key = request.headers.get("Idempotency-Key", "")
            require(
                8 <= len(key) <= 200,
                "idempotency_key_required",
                "Supply an Idempotency-Key of 8–200 characters.",
                400,
            )
            digest = hashlib.sha256(
                json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            # Resource identity is part of semantic intent, not just request body.
            digest = hashlib.sha256((request.path + ":" + digest).encode()).hexdigest()
            with transaction.atomic():
                receipt, _ = CommandReceipt.objects.get_or_create(
                    principal=request.user,
                    operation=operation,
                    key=key,
                    defaults={"payload_hash": digest},
                )
                receipt = CommandReceipt.objects.select_for_update().get(pk=receipt.pk)
                require(
                    receipt.payload_hash == digest,
                    "idempotency_conflict",
                    "This key was already used for a different request.",
                )
                if receipt.response is not None:
                    # Execute the same object authorization boundary before disclosing a receipt.
                    from .permissions import authorize_replay

                    authorize_replay(
                        request,
                        operation,
                        tuple(a for a in args if a is not None),
                        receipt.response,
                    )
                    return receipt.response, receipt.status_code
                try:
                    with transaction.atomic():
                        data, status = fn(request, payload, *args, **kwargs)
                except DomainError as error:
                    data, status = (
                        {"code": error.code, "message": error.message, "fields": error.fields},
                        error.status,
                    )
                receipt.response, receipt.status_code = data, status
                receipt.save(update_fields=["response", "status_code"])
                return data, status

        return execute

    return decorate


def vehicle_input(data, user):
    make = Taxonomy.objects.get(pk=data["make_id"], kind="make")
    model = Taxonomy.objects.get(pk=data["model_id"], kind="model", parent=make)
    require(
        1886 <= data["year"] <= timezone.now().year + 1,
        "invalid_year",
        "Select a valid model year.",
        422,
    )
    return Vehicle.objects.create(
        owner=user,
        make=make,
        model=model,
        year=data["year"],
        mileage=data["mileage"],
        mileage_unit=data["mileage_unit"],
    )


@command("createSellerLead")
def create_lead(request, data):
    role(request.user, "ROLE-002")
    require(
        request.user.contact_verified,
        "contact_unverified",
        "Verify your contact before submitting.",
        403,
    )
    vehicle = vehicle_input(data["vehicle"], request.user)
    advisor = (
        User.objects.filter(is_active=True, roles__contains=["ROLE-011"])
        .order_by("date_joined")
        .first()
    )
    lead = Lead.objects.create(
        owner=request.user,
        vehicle=vehicle,
        contact=data["contact"],
        consent=data["consent"],
        assigned_to=advisor,
    )
    emit(request.user, "seller.lead_created", lead, [request.user.id])
    return {"id": str(lead.id), "status": lead.status, "version": lead.version}, 201


def appointment_dto(a):
    return {
        "id": str(a.id),
        "lead_id": str(a.lead_id),
        "branch_id": str(a.slot.branch_id),
        "slot_id": str(a.slot_id),
        "starts_at": a.slot.starts_at.isoformat().replace("+00:00", "Z"),
        "timezone": a.slot.branch.timezone,
        "ends_at": a.slot.ends_at.isoformat().replace("+00:00", "Z"),
        "status": a.status,
        "version": a.version,
    }


@command("createAppointment")
def book(request, data):
    role(request.user, "ROLE-002", "ROLE-006")
    slot = Slot.objects.select_for_update().select_related("branch").get(pk=data["slot_id"])
    require(
        str(slot.branch_id) == data["branch_id"],
        "branch_mismatch",
        "The slot must belong to the selected branch.",
        422,
    )
    lead = Lead.objects.select_for_update().get(pk=data["lead_id"])
    if "ROLE-002" in request.user.roles:
        own(request.user, lead.owner_id)
    else:
        branch_scope(request.user, slot.branch_id)
    require(
        lead.status in ["eligible", "in_progress"],
        "lead_not_eligible",
        "This selling request must be qualified before booking.",
    )
    require(
        slot.branch.active and slot.starts_at > db_now() and slot.reserved < slot.capacity,
        "slot_unavailable",
        "This slot is no longer available. Choose another time.",
    )
    require(
        not Appointment.objects.filter(lead=lead, status__in=["confirmed", "checked_in"]).exists(),
        "appointment_exists",
        "This request already has an active appointment.",
    )
    slot.reserved += 1
    slot.save(update_fields=["reserved"])
    appt = Appointment.objects.create(lead=lead, slot=slot)
    emit(request.user, "appointment.confirmed", appt, [lead.owner_id])
    return appointment_dto(appt), 201


@command("transitionAppointment")
def appointment_transition(request, data, pk):
    # Lock slots in stable order before the appointment to match creation capacity ownership.
    current = Appointment.objects.get(pk=pk)
    ids = sorted({str(current.slot_id), str(data.get("slot_id", current.slot_id))})
    slots = {
        str(s.id): s for s in Slot.objects.select_for_update().filter(id__in=ids).order_by("id")
    }
    a = Appointment.objects.select_for_update().select_related("lead", "slot").get(pk=pk)
    require(
        str(a.slot_id) in slots, "concurrent_reschedule", "This appointment changed. Refresh it."
    )
    version(request, a)
    action = data["action"]
    if action in ["cancel", "reschedule"]:
        role(request.user, "ROLE-002", "ROLE-006")
        if "ROLE-002" in request.user.roles:
            own(request.user, a.lead.owner_id)
        else:
            branch_scope(request.user, a.slot.branch_id)
        require(
            a.status == "confirmed", "invalid_transition", "Only a confirmed visit can be changed."
        )
        old = slots[str(a.slot_id)]
        if action == "reschedule":
            new = slots[data["slot_id"]]
            require(
                new.starts_at > db_now()
                and new.branch.active
                and (new.id == old.id or new.reserved < new.capacity),
                "slot_unavailable",
                "Choose another available slot.",
            )
            if new.id != old.id:
                new.reserved += 1
                new.save(update_fields=["reserved"])
                old.reserved -= 1
                old.save(update_fields=["reserved"])
                a.slot = new
        else:
            old.reserved -= 1
            old.save(update_fields=["reserved"])
            a.status = "cancelled"
    else:
        role(request.user, "ROLE-006")
        branch_scope(request.user, a.slot.branch_id)
        allowed = {
            "check-in": ("confirmed", "checked_in"),
            "complete": ("checked_in", "completed"),
            "mark-no-show": ("confirmed", "no_show"),
        }
        require(
            action in allowed and a.status == allowed[action][0],
            "invalid_transition",
            "This visit cannot take that action.",
        )
        if action == "mark-no-show":
            require(
                db_now() >= a.slot.starts_at + timedelta(minutes=15),
                "too_early",
                "The arrival grace interval has not elapsed.",
            )
        a.status = allowed[action][1]
    a.version += 1
    a.save()
    emit(request.user, "appointment." + action, a, [a.lead.owner_id])
    return appointment_dto(a), 200


def eligible_member(user, lock=False):
    member = Membership.objects.filter(user=user, active=True, can_bid=True).first()
    require(
        member is not None, "dealer_ineligible", "An active dealer bidding grant is required.", 403
    )
    orgs = Organization.objects.select_for_update() if lock else Organization.objects
    org = orgs.get(pk=member.organization_id)
    members = Membership.objects.select_for_update() if lock else Membership.objects
    member = members.get(pk=member.pk)
    require(
        org.status == "active" and member.active and member.can_bid,
        "dealer_ineligible",
        "This dealer account cannot bid.",
        403,
    )
    return member


def public_vehicle(v):
    return {
        "make_id": str(v.make_id),
        "model_id": str(v.model_id),
        "make_name": v.make.name,
        "model_name": v.model.name,
        "year": v.year,
        "mileage": v.mileage,
        "mileage_unit": v.mileage_unit,
        "body_type": v.details.get("body_type", "Unknown"),
        "transmission": v.details.get("transmission", "unknown"),
        "fuel_type": v.details.get("fuel_type", "unknown"),
    }


def auction_dto(a):
    return {
        "id": str(a.pk),
        "status": a.status,
        "currency": a.currency,
        "current_bid_minor": a.current_bid_minor,
        "sequence": a.sequence,
        "version": a.version,
        "minimum_next_bid_minor": (
            a.current_bid_minor + a.increment_minor if a.current_bid_minor else a.starting_minor
        )
        if a.status == "open" and not a.safety_hold
        else None,
        "increment_minor": a.increment_minor,
        "server_time": timezone.now().isoformat().replace("+00:00", "Z"),
        "closes_at": a.closes_at.isoformat().replace("+00:00", "Z"),
        "report_revision_id": str(a.report_id),
        "vehicle": public_vehicle(a.vehicle),
        "public_media": a.vehicle.details.get("media", []),
    }


@command("submitBid")
def bid(request, data, pk):
    role(request.user, "ROLE-004")
    member = eligible_member(request.user, lock=True)
    a = Auction.objects.select_for_update().get(pk=pk)
    now = db_now()
    require(
        a.status == "open" and not a.safety_hold and a.starts_at <= now < a.closes_at,
        "auction_not_open",
        "This auction is not accepting bids.",
    )
    amount = money(data["amount_minor"])
    require(data["currency"] == a.currency, "currency_mismatch", "Use the auction currency.", 422)
    minimum = (
        a.starting_minor if a.current_bid_minor is None else a.current_bid_minor + a.increment_minor
    )
    require(
        amount >= minimum and (amount - a.starting_minor) % a.increment_minor == 0,
        "bid_too_low",
        "Your bid must meet the current minimum and increment.",
    )
    a.sequence += 1
    a.version += 1
    a.current_bid_minor = amount
    accepted = Bid.objects.create(
        auction=a, membership=member, amount_minor=amount, sequence=a.sequence, accepted_at=now
    )
    a.save()
    emit(request.user, "auction.bid_accepted", a, [request.user.id])
    return {
        "bid_id": str(accepted.id),
        "auction_id": str(a.id),
        "status": "accepted",
        "amount_minor": amount,
        "currency": a.currency,
        "sequence": a.sequence,
        "accepted_at": now.isoformat().replace("+00:00", "Z"),
    }, 201


def close_locked(user, a):
    existing = Result.objects.filter(auction=a).first()
    if existing:
        return existing
    require(
        a.status in ["open", "paused"] and db_now() >= a.closes_at,
        "cannot_close",
        "The auction deadline has not elapsed or its state does not allow closing.",
    )
    winner = Bid.objects.filter(auction=a).order_by("-sequence").first()
    status = "no_bid" if not winner else "pending_seller_decision"
    if winner and a.reserve_minor and winner.amount_minor < a.reserve_minor:
        status, winner = "no_qualifying_bid", None
    if a.safety_hold or a.status == "paused":
        status, winner = "pending_review", None
    result = Result.objects.create(auction=a, winner=winner, status=status)
    a.status, a.version = "closed", a.version + 1
    a.save()
    emit(user, "auction.closed", a, [a.vehicle.owner_id])
    return result


def result_dto(r):
    return {
        "id": str(r.pk),
        "auction_id": str(r.auction_id),
        "status": r.status,
        "winning_bid_id": str(r.winner_id) if r.winner_id else None,
        "version": r.version,
    }


@command("closeAuction")
def close(request, data, pk):
    role(request.user, "ROLE-010")
    a = Auction.objects.select_for_update().get(pk=pk)
    branch_scope(request.user, a.report.inspection.branch_id)
    version(request, a)
    return result_dto(close_locked(request.user, a)), 200


@command("recordSellerDecision")
def seller_decision(request, data, pk):
    r = (
        Result.objects.select_for_update(of=("self",))
        .select_related("auction__vehicle", "winner__membership")
        .get(pk=pk)
    )
    own(request.user, r.auction.vehicle.owner_id)
    version(request, r)
    require(
        r.status == "pending_seller_decision"
        and not r.seller_decision
        and db_now() < r.auction.offer_expires_at
        and data["offer_version"] == r.version,
        "offer_unavailable",
        "This offer is expired, changed or already decided.",
    )
    r.seller_decision = data["decision"]
    r.version += 1
    r.save()
    output = {
        "id": str(r.id),
        "status": "accepted" if r.seller_decision == "accept" else "rejected",
        "recorded_at": timezone.now().isoformat().replace("+00:00", "Z"),
        "version": r.version,
    }
    if r.seller_decision == "accept":
        member = r.winner.membership
        case = TransactionCase.objects.create(
            result=r,
            branch=r.auction.report.inspection.branch,
            vehicle=r.auction.vehicle,
            seller=request.user,
            buyer=member.user,
            organization=member.organization,
        )
        Record.objects.create(
            kind="OwnershipTransfer",
            status="pending",
            owner=request.user,
            organization=member.organization,
            branch=r.auction.report.inspection.branch,
            prepared_by=request.user,
            data={"transaction_id": str(case.id)},
        )
        output["transaction_id"] = str(case.id)
    emit(request.user, "seller.decision_recorded", r, [request.user.id])
    return output, 201


def clean_evidence(user, file_id):
    from .permissions import record_access

    f = Record.objects.get(pk=file_id, kind="File")
    record_access(user, f)
    require(
        f.status == "clean", "evidence_not_clean", "Attach a processed, clean evidence file.", 422
    )
    return f


def complete_findings(template, findings):
    points = {str(p["id"]): p for p in template.data["points"]}
    submitted = {f["point_id"]: f for f in findings}
    require(
        len(submitted) == len(findings),
        "duplicate_point",
        "Each inspection point can appear once.",
        422,
    )
    require(
        set(submitted) <= set(points),
        "unknown_point",
        "Use the assigned template's inspection points.",
        422,
    )
    for pid, point in points.items():
        if point["required"]:
            require(
                pid in submitted,
                "incomplete_report",
                "Complete every required inspection point.",
                422,
            )
        f = submitted.get(pid)
        if not f:
            continue
        require(
            f["result"] in point["allowed_results"],
            "invalid_finding",
            "This result is not permitted for that point.",
            422,
        )
        if f["result"] in ["unknown", "not_applicable"]:
            require(
                bool(f.get("comment", "").strip()),
                "finding_reason_required",
                "Explain unknown or not applicable findings.",
                422,
            )
        if f["result"] == "defect":
            require(
                f.get("severity") in ["minor", "major", "critical"],
                "severity_required",
                "Classify the defect severity.",
                422,
            )
            if point.get("evidence_required_on_defect"):
                require(
                    bool(f.get("evidence_ids")),
                    "evidence_required",
                    "Attach evidence for this defect.",
                    422,
                )


@command("createInspectionRevision")
def create_revision(request, data, pk):
    i = Inspection.objects.select_for_update().get(pk=pk)
    role(request.user, "ROLE-007")
    own(request.user, i.inspector_id)
    branch_scope(request.user, i.branch_id)
    version(request, i)
    require(
        i.status in ["draft", "returned"],
        "immutable_report",
        "Published or submitted reports cannot be edited.",
    )
    require(
        str(i.template_id) == data["template_version_id"],
        "template_changed",
        "Use the assigned checklist version.",
        422,
    )
    complete_findings(i.template, data["findings"])
    for finding in data["findings"]:
        for file_id in finding.get("evidence_ids", []):
            clean_evidence(request.user, file_id)
    number = (Revision.objects.filter(inspection=i).aggregate(n=models_max("number"))["n"] or 0) + 1
    r = Revision.objects.create(
        inspection=i,
        number=number,
        author=request.user,
        findings=data["findings"],
        checksum=hashlib.sha256(json.dumps(data["findings"], sort_keys=True).encode()).hexdigest(),
    )
    i.version += 1
    i.save()
    emit(request.user, "inspection.revision_created", i)
    return revision_dto(r), 201


def models_max(field):
    from django.db.models import Max

    return Max(field)


def revision_dto(r):
    return {
        "id": str(r.id),
        "inspection_id": str(r.inspection_id),
        "status": r.status,
        "version": r.version,
        "template_version_id": str(r.inspection.template_id),
        "findings": r.findings,
        "checksum": r.checksum,
        **(
            {"published_at": r.published_at.isoformat().replace("+00:00", "Z")}
            if r.published_at
            else {}
        ),
    }


@command("publishInspection")
def publish(request, data, pk):
    role(request.user, "ROLE-008")
    i = Inspection.objects.select_for_update().get(pk=pk)
    branch_scope(request.user, i.branch_id)
    version(request, i)
    r = Revision.objects.select_for_update().filter(inspection=i).order_by("-number").first()
    require(
        r is not None and i.status == "submitted",
        "report_not_submitted",
        "Submit a complete revision before publication.",
    )
    require(
        str(r.id) == data["revision_id"], "stale_revision", "Review the current report revision."
    )
    require(
        r.author_id != request.user.id,
        "independent_review_required",
        "The report author cannot publish their own report.",
        403,
    )
    complete_findings(i.template, r.findings)
    for finding in r.findings:
        for file_id in finding.get("evidence_ids", []):
            clean_evidence(request.user, file_id)
    r.status, r.reviewer, r.published_at = "published", request.user, timezone.now()
    r.version += 1
    r.save()
    i.status, i.version = "published", i.version + 1
    i.save()
    emit(request.user, "inspection.report_published", i, [i.vehicle.owner_id])
    return revision_dto(r), 200


@command("approveReconciliation")
def approve_reconciliation(request, data, pk):
    role(request.user, "ROLE-014")
    fresh(request, "finance")
    r = Record.objects.select_for_update().get(pk=pk, kind="Reconciliation")
    from .permissions import record_access

    record_access(request.user, r)
    version(request, r)
    require(
        r.prepared_by_id != request.user.id,
        "independent_review_required",
        "A preparer cannot approve their own reconciliation.",
        403,
    )
    require(
        r.status == "prepared", "already_reviewed", "This reconciliation has already been reviewed."
    )
    o = Obligation.objects.select_for_update().get(pk=r.data["obligation_id"])
    evidence = list(PaymentEvidence.objects.select_for_update().filter(obligation=o))
    require(
        set(data["evidence_ids"]) == set(r.data["evidence_ids"]) == {str(e.id) for e in evidence},
        "evidence_changed",
        "Review the current evidence set before approving.",
    )
    total = sum(e.amount_minor for e in evidence)
    require(
        evidence and total == o.amount_minor and all(e.currency == o.currency for e in evidence),
        "reconciliation_mismatch",
        "Evidence must exactly match the obligation amount and currency.",
    )
    require(
        all(e.prepared_by_id != request.user.id for e in evidence),
        "independent_review_required",
        "Evidence requires an independent reviewer.",
        403,
    )
    for e in evidence:
        clean_evidence(request.user, e.file_id)
        e.verified_by = request.user
        e.save()
    r.status, r.reviewed_by, r.version = "approved", request.user, r.version + 1
    r.save()
    o.status, o.version = "reconciled", o.version + 1
    o.save()
    emit(
        request.user, "settlement.reconciled", o, [o.transaction.seller_id, o.transaction.buyer_id]
    )
    return {"id": str(r.id), "status": "reconciled", "version": r.version}, 200
