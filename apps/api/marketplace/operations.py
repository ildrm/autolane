"""Supporting business commands with explicit policy and evidence boundaries."""

from uuid import uuid4
from .models import Vehicle
from django.utils import timezone
from . import domain as d, services as s
from .models import (
    Membership,
    Obligation,
    Organization,
    PaymentEvidence,
    Record,
    TransactionCase,
)
from .permissions import case_access, record_access


@d.command("decideDealerVerification")
def dealer_decision(request, data, pk):
    return s.record_transition.__wrapped__(
        request, {"action": data["decision"], "reason": data["reason"]}, pk
    )


@d.command("createDealerVerification")
def create_verification(request, data, pk=None):
    d.role(request.user, "ROLE-005")
    member = Membership.objects.select_for_update().get(
        user=request.user, organization_id=data["organization_id"], active=True
    )
    d.require(
        member.organization.status in ["pending", "rejected"],
        "verification_not_needed",
        "This organization does not need a new application.",
    )
    d.require(
        not Record.objects.filter(
            kind="DealerVerification",
            organization=member.organization,
            status__in=["submitted", "needs_evidence"],
        ).exists(),
        "verification_exists",
        "This organization has an open verification.",
    )
    for fid in data["evidence_ids"]:
        d.clean_evidence(request.user, fid)
    r = Record.objects.create(
        kind="DealerVerification",
        owner=request.user,
        prepared_by=request.user,
        organization=member.organization,
        status="submitted",
        data=data,
    )
    d.emit(request.user, "dealer.verification_submitted", r, [request.user.id])
    return s.dto(r), 201


@d.command("withdrawConsumerOffer")
def withdraw_offer(request, data, pk):
    current = Record.objects.get(pk=pk, kind="ConsumerOffer")
    vehicle = Vehicle.objects.select_for_update().get(pk=current.vehicle_id)
    r = Record.objects.select_for_update().get(pk=pk, kind="ConsumerOffer")
    if request.user.id != vehicle.owner_id:
        d.role(request.user, "ROLE-021", "ROLE-011")
        d.branch_scope(request.user, r.branch_id)
    d.version(request, r)
    d.require(
        r.status == "issued",
        "offer_already_decided",
        "An accepted or expired offer cannot be withdrawn.",
    )
    r.status = "withdrawn"
    r.version += 1
    r.data["withdrawal_reason"] = data["reason"]
    r.save()
    d.emit(request.user, "consumer.offer_withdrawn", r, [r.owner_id])
    return s.dto(r), 200


@d.command("actOnProcurement")
def procurement_action(request, data, pk):
    r = Record.objects.select_for_update().get(pk=pk, kind="ProcurementRequest")
    record_access(request.user, r)
    d.version(request, r)
    action = data["action"]
    allowed = {
        "assign": (["submitted"], "assigned"),
        "present_proposal": (["assigned", "matching", "proposal_presented"], "proposal_presented"),
        "select": (["proposal_presented"], "selected"),
        "fulfil": (["selected"], "fulfilled"),
        "cancel": (
            ["submitted", "assigned", "matching", "proposal_presented", "selected"],
            "cancelled",
        ),
    }
    d.require(
        r.status in allowed[action][0],
        "invalid_transition",
        "This sourcing request cannot take that action.",
    )
    if action in ["select", "cancel"]:
        d.own(request.user, r.owner_id)
    else:
        d.role(request.user, "ROLE-011")
    if action == "assign":
        from .models import User

        advisor = User.objects.get(
            pk=data["advisor_id"], is_active=True, roles__contains=["ROLE-011"]
        )
        r.data["assigned_to"] = str(advisor.id)
        r.data["advisor_id"] = str(advisor.id)
    if action in ["present_proposal", "select"]:
        listing = Record.objects.get(
            pk=data["candidate_listing_id"], kind="VehicleListing", status="available"
        )
        d.require(
            not listing.vehicle.channel,
            "listing_unavailable",
            "The proposed vehicle is already committed.",
        )
        if action == "select":
            d.require(
                str(listing.id) == r.data.get("candidate_listing_id"),
                "proposal_changed",
                "Select the currently presented proposal.",
            )
        r.data["candidate_listing_id"] = str(listing.id)
    if action == "fulfil":
        listing = Record.objects.get(pk=r.data["candidate_listing_id"])
        d.require(
            TransactionCase.objects.filter(
                vehicle=listing.vehicle, buyer=r.owner, status="closed"
            ).exists(),
            "transaction_incomplete",
            "Complete the linked vehicle transaction before fulfilling this request.",
        )
    r.status = allowed[action][1]
    r.version += 1
    r.data["last_reason"] = data["reason"]
    r.save()
    d.emit(request.user, "procurement." + action, r, [r.owner_id])
    return s.dto(r), 200


@d.command("actOnCampaign")
def campaign_action(request, data, pk):
    d.role(request.user, "ROLE-025")
    r = Record.objects.select_for_update().get(pk=pk, kind="Campaign")
    d.version(request, r)
    action = data["action"]
    rules = {
        "submit_review": (["draft"], "review"),
        "approve": (["review"], "approved"),
        "schedule": (["approved"], "scheduled"),
        "stop": (["scheduled", "running"], "stopped"),
    }
    d.require(
        r.status in rules[action][0], "invalid_transition", "This campaign cannot take that action."
    )
    if action == "approve":
        d.require(
            r.prepared_by_id != request.user.id,
            "independent_review_required",
            "An independent growth reviewer is required.",
            403,
        )
        r.reviewed_by = request.user
    if action == "schedule":
        # Do not claim a dispatched campaign without an approved outbound adapter.
        raise d.DomainError(
            "provider_not_configured",
            "Configure and verify a consent-aware messaging provider before scheduling this campaign.",
            503,
        )
    r.status = rules[action][1]
    r.version += 1
    r.save()
    d.emit(request.user, "campaign." + action, r)
    return s.dto(r), 200


@d.command("recordSignatureEvidence")
def signature(request, data, pk):
    d.role(request.user, "ROLE-012")
    d.fresh(request, "legal")
    r = Record.objects.select_for_update().get(pk=pk, kind="Contract")
    record_access(request.user, r, write=True)
    d.version(request, r)
    d.require(
        r.status in ["issued", "partially_signed"],
        "contract_not_issued",
        "Issue the reviewed contract before recording signatures.",
    )
    d.require(
        data["document_version_id"] == r.data["document_version_id"],
        "document_mismatch",
        "The signature must refer to the exact issued document.",
        422,
    )
    d.require(
        data["signer_id"] in r.data["required_signer_ids"],
        "invalid_signer",
        "This signer is not a required contract party.",
        422,
    )
    from django.utils.dateparse import parse_datetime

    d.require(
        parse_datetime(data["signed_at"]) <= timezone.now(),
        "invalid_signature_time",
        "A signature cannot occur in the future.",
        422,
    )
    d.clean_evidence(request.user, data["evidence_id"])
    signatures = r.data.get("signatures", [])
    d.require(
        not any(v["signer_id"] == data["signer_id"] for v in signatures),
        "signature_recorded",
        "This signer's evidence has already been recorded.",
    )
    signatures.append(
        {
            **data,
            "recorded_by": str(request.user.id),
            "document_checksum": r.data["document_checksum"],
        }
    )
    r.data["signatures"] = signatures
    r.status = (
        "signed"
        if {v["signer_id"] for v in signatures} == set(r.data["required_signer_ids"])
        else "partially_signed"
    )
    r.version += 1
    r.save()
    d.emit(request.user, "contract." + r.status, r, r.data["required_signer_ids"])
    return {"id": str(r.id), "version": r.version, "status": r.status}, 200


@d.command("recordDeliveryHandover")
def handover(request, data, pk):
    d.role(request.user, "ROLE-020", "ROLE-018")
    r = Record.objects.select_for_update().get(pk=pk, kind="Delivery")
    record_access(request.user, r, write=True)
    d.version(request, r)
    case = TransactionCase.objects.select_for_update().get(pk=r.data["transaction_id"])
    case_access(request.user, case)
    d.require(
        r.status in (["assigned"] if data["kind"] == "pickup" else ["in_transit"]),
        "invalid_handover",
        "This delivery is not at that custody stage.",
    )
    if data["kind"] == "delivery":
        d.require(
            case.title_verified
            and Obligation.objects.filter(transaction=case).exists()
            and not Obligation.objects.filter(transaction=case)
            .exclude(status="reconciled")
            .exists(),
            "delivery_prerequisites_missing",
            "Verify title and reconcile required obligations before final delivery.",
        )
        d.require(
            str(case.buyer_id) == data["to_party_id"],
            "recipient_mismatch",
            "The recipient must match the authorized buyer.",
            422,
        )
    for fid in data["evidence_ids"]:
        d.clean_evidence(request.user, fid)
    r.data.setdefault("handovers", []).append(data)
    r.status, r.version = ("collected" if data["kind"] == "pickup" else "delivered"), r.version + 1
    r.save()
    if data["kind"] == "delivery":
        case.handover_verified, case.version = True, case.version + 1
        case.save()
    d.emit(request.user, "vehicle.handover_recorded", r, [case.seller_id, case.buyer_id])
    return {"id": str(r.id), "status": r.status, "version": r.version}, 200


@d.command("createConsumerOffer")
def consumer_offer(request, data, pk=None):
    d.role(request.user, "ROLE-021", "ROLE-011")
    listing = Record.objects.select_for_update().get(pk=data["listing_id"], kind="VehicleListing")
    record_access(request.user, listing, write=True)
    d.require(
        listing.status == "available"
        and listing.version == data["listing_version"]
        and not listing.vehicle.channel,
        "listing_unavailable",
        "The current listing is not available.",
    )
    inquiry = Record.objects.get(
        pk=data["purchase_request_id"], kind="PurchaseRequest", owner_id=data["buyer_id"]
    )
    d.require(
        inquiry.data["listing_id"] == str(listing.id),
        "inquiry_mismatch",
        "The buyer inquiry must refer to this vehicle.",
        422,
    )
    d.require(
        data["currency"] == listing.data["currency"],
        "currency_mismatch",
        "Use the listing currency.",
        422,
    )
    d.money(data["amount_minor"])
    d.clean_evidence(request.user, data["seller_authorization_evidence_id"])
    from django.utils.dateparse import parse_datetime

    d.require(
        parse_datetime(data["expires_at"]) > timezone.now(),
        "invalid_expiry",
        "Offer expiry must be in the future.",
        422,
    )
    r = Record.objects.create(
        kind="ConsumerOffer",
        owner=inquiry.owner,
        prepared_by=request.user,
        branch=listing.branch,
        vehicle=listing.vehicle,
        status="issued",
        data=data,
    )
    d.emit(request.user, "consumer.offer_issued", r, [inquiry.owner_id])
    return s.dto(r), 201


@d.command("acceptConsumerOffer")
def accept_offer(request, data, pk):
    original = Record.objects.get(pk=pk, kind="ConsumerOffer")
    vehicle = Vehicle.objects.select_for_update().get(pk=original.vehicle_id)
    offer = Record.objects.select_for_update().get(pk=pk, kind="ConsumerOffer")
    d.own(request.user, offer.owner_id)
    d.fresh(request, "consumer_offer")
    d.version(request, offer)
    listing = Record.objects.select_for_update().get(
        pk=offer.data["listing_id"], kind="VehicleListing"
    )
    from django.utils.dateparse import parse_datetime

    d.require(
        offer.status == "issued"
        and parse_datetime(offer.data["expires_at"]) > d.db_now()
        and offer.data["terms_version"] == data["terms_version"]
        and listing.status == "available"
        and not vehicle.channel,
        "offer_unavailable",
        "This offer or vehicle is no longer available.",
    )
    vehicle.channel = "consumer"
    vehicle.save()
    offer.status, offer.version = "accepted", offer.version + 1
    case = TransactionCase.objects.create(
        consumer_offer=offer,
        branch=listing.branch,
        vehicle=vehicle,
        seller=vehicle.owner,
        buyer=request.user,
    )
    offer.data.update(transaction_id=str(case.id), consent=data["consent"])
    offer.save()
    listing.status, listing.version = "unavailable", listing.version + 1
    listing.save()
    Record.objects.create(
        kind="OwnershipTransfer",
        status="pending",
        owner=vehicle.owner,
        branch=listing.branch,
        prepared_by=request.user,
        data={"transaction_id": str(case.id)},
    )
    inquiry = Record.objects.select_for_update().get(pk=offer.data["purchase_request_id"])
    inquiry.data["transaction_id"] = str(case.id)
    inquiry.save()
    d.emit(request.user, "consumer.offer_accepted", offer, [vehicle.owner_id, request.user.id])
    return {
        "id": str(offer.id),
        "status": "accepted",
        "recorded_at": timezone.now().isoformat().replace("+00:00", "Z"),
        "version": offer.version,
        "transaction_id": str(case.id),
    }, 201


@d.command("submitDealerApplication")
def dealer_application(request, data, pk=None):
    d.require(
        request.user.contact_verified, "contact_unverified", "Verify your contact first.", 403
    )
    for fid in data["evidence_ids"]:
        d.clean_evidence(request.user, fid)
    org = Organization.objects.create(
        legal_name=data["legal_name"],
        jurisdiction=data["jurisdiction"],
        registration_number=data["registration_number"],
    )
    Membership.objects.create(user=request.user, organization=org, active=True, can_bid=False)
    if "ROLE-005" not in request.user.roles:
        request.user.roles = [*request.user.roles, "ROLE-005"]
        request.user.save(update_fields=["roles"])
    r = Record.objects.create(
        kind="DealerVerification",
        owner=request.user,
        prepared_by=request.user,
        organization=org,
        status="submitted",
        data={**data, "organization_id": str(org.id)},
    )
    d.emit(request.user, "dealer.application_submitted", r, [request.user.id])
    return s.dto(r), 201


@d.command("createPaymentObligation")
def create_obligation(request, data, pk=None):
    d.role(request.user, "ROLE-013")
    case = TransactionCase.objects.get(pk=data["transaction_id"])
    case_access(request.user, case)
    o = Obligation.objects.create(
        transaction=case,
        amount_minor=d.money(data["amount_minor"]),
        currency=data["currency"],
        prepared_by=request.user,
        data=data,
    )
    d.emit(request.user, "obligation.created", o, [case.seller_id, case.buyer_id])
    return s.dto(o), 201


@d.command("submitPaymentEvidence")
def payment_evidence(request, data, pk):
    d.role(request.user, "ROLE-013")
    o = Obligation.objects.select_for_update().get(pk=pk)
    case_access(request.user, o.transaction)
    d.version(request, o)
    d.require(
        o.status in ["outstanding", "partially_satisfied", "disputed"],
        "invalid_state",
        "This obligation cannot accept new evidence.",
    )
    d.require(
        data["currency"] == o.currency,
        "currency_mismatch",
        "Evidence currency must match the obligation.",
        422,
    )
    for key in ["payer_party_id", "payee_party_id"]:
        d.require(
            data[key] == o.data.get(key),
            "party_mismatch",
            "Payment parties must match the obligation.",
            422,
        )
    f = d.clean_evidence(request.user, data["evidence_id"])
    source = str(data.get("source_id", "manual")) + ":" + data["external_reference"]
    evidence = PaymentEvidence.objects.create(
        obligation=o,
        source_reference=source,
        amount_minor=d.money(data["amount_minor"]),
        currency=data["currency"],
        file=f,
        prepared_by=request.user,
    )
    o.status, o.version = "evidence_pending", o.version + 1
    o.save()
    d.emit(request.user, "obligation.evidence_submitted", o)
    return {"id": str(evidence.id), "status": "pending_review", "version": evidence.version}, 202


@d.command("prepareReconciliation")
def prepare_reconciliation(request, data, pk=None):
    d.role(request.user, "ROLE-013")
    o = Obligation.objects.select_for_update().get(pk=data["obligation_id"])
    case_access(request.user, o.transaction)
    d.require(
        o.transaction.branch_id is not None,
        "branch_required",
        "A scoped transaction branch is required.",
    )
    r = Record.objects.create(
        kind="Reconciliation",
        owner=request.user,
        prepared_by=request.user,
        branch=o.transaction.branch,
        data=data,
        status="prepared",
    )
    d.emit(request.user, "reconciliation.prepared", r)
    return s.dto(r), 201


@d.command("verifyOwnershipTransfer")
def verify_transfer(request, data, pk):
    d.role(request.user, "ROLE-012")
    d.fresh(request, "legal")
    r = Record.objects.select_for_update().get(pk=pk, kind="OwnershipTransfer")
    record_access(request.user, r, write=True)
    d.version(request, r)
    d.require(
        r.prepared_by_id != request.user.id,
        "independent_review_required",
        "Independent verification is required.",
        403,
    )
    for fid in data.get("evidence_ids", []):
        d.clean_evidence(request.user, fid)
    d.require(
        bool(data.get("evidence_ids")),
        "evidence_required",
        "Provide transfer authority evidence.",
        422,
    )
    case = TransactionCase.objects.select_for_update().get(pk=r.data["transaction_id"])
    r.status, r.version, r.reviewed_by = "verified", r.version + 1, request.user
    r.data["evidence_ids"] = data["evidence_ids"]
    r.save()
    case.title_verified, case.version = True, case.version + 1
    case.save()
    d.emit(request.user, "ownership.transfer_verified", r, [case.seller_id, case.buyer_id])
    return s.dto(r), 200


@d.command("closeTransaction")
def close_transaction(request, data, pk):
    d.role(request.user, "ROLE-012")
    case = TransactionCase.objects.select_for_update().get(pk=pk)
    case_access(request.user, case)
    d.version(request, case)
    contracts = Record.objects.filter(kind="Contract", data__transaction_id=str(case.id))
    obligations = Obligation.objects.filter(transaction=case)
    d.require(
        contracts.filter(status="signed").exists()
        and obligations.exists()
        and not obligations.exclude(status="reconciled").exists()
        and case.title_verified
        and case.handover_verified,
        "closure_evidence_missing",
        "A signed contract, reconciled obligations, verified title and handover are required.",
    )
    d.require(
        not Record.objects.filter(
            kind__in=["SupportTicket", "WarrantyClaim"], data__transaction_id=str(case.id)
        )
        .exclude(status__in=["closed", "withdrawn"])
        .exists(),
        "unresolved_dispute",
        "Resolve transaction disputes before closing.",
    )
    case.status, case.version = "closed", case.version + 1
    case.save()
    d.emit(request.user, "transaction.closed", case, [case.seller_id, case.buyer_id])
    return s.dto(case), 200


@d.command("actOnContent")
def content_action(request, data, pk):
    d.role(request.user, "ROLE-015")
    r = Record.objects.select_for_update().get(pk=pk, kind="Content")
    d.version(request, r)
    d.require(
        data["revision_id"] == r.data["revision_id"],
        "stale_revision",
        "Review the current content revision.",
    )
    act = data["action"]
    mapping = {
        "submit_review": (["draft"], "review"),
        "approve": (["review"], "approved"),
        "publish": (["approved", "scheduled"], "published"),
        "schedule": (["approved"], "scheduled"),
        "retire": (["published"], "retired"),
    }
    d.require(
        r.status in mapping[act][0], "invalid_transition", "This content cannot take that action."
    )
    if act == "approve":
        d.require(
            r.prepared_by_id != request.user.id,
            "independent_review_required",
            "The author cannot approve their revision.",
            403,
        )
        r.reviewed_by = request.user
    if act in ["publish", "schedule"]:
        d.require(
            r.reviewed_by_id is not None and r.reviewed_by_id != r.prepared_by_id,
            "review_required",
            "Independent approval is required.",
        )
        if act == "schedule":
            d.require(
                bool(data.get("publish_at")), "schedule_required", "Choose a publication time.", 422
            )
            r.data["publish_at"] = data["publish_at"]
        if act == "publish":
            r.data["published_at"] = timezone.now().isoformat().replace("+00:00", "Z")
    r.status, r.version = mapping[act][1], r.version + 1
    r.save()
    d.emit(request.user, "content." + act, r)
    return s.dto(r), 200


@d.command("reviseContent")
def revise_content(request, data, pk):
    d.role(request.user, "ROLE-015")
    r = Record.objects.select_for_update().get(pk=pk, kind="Content")
    d.version(request, r)
    d.require(
        r.status != "published",
        "published_revision",
        "Retire or create a successor before editing published content.",
    )
    r.data = {"content": data, "revision_id": str(uuid4())}
    r.status, r.version, r.prepared_by, r.reviewed_by = "draft", r.version + 1, request.user, None
    r.save()
    d.emit(request.user, "content.revised", r)
    return s.dto(r), 200


@d.command("createPolicyVersion")
def create_policy(request, data, pk):
    d.role(request.user, "ROLE-016")
    d.fresh(request, "policy")
    original = Record.objects.select_for_update().get(pk=pk, kind="Policy")
    d.version(request, original)
    r = Record.objects.create(
        kind="Policy",
        owner=request.user,
        prepared_by=request.user,
        parent=original,
        data=data,
        status="draft",
    )
    d.emit(request.user, "policy.version_proposed", r)
    return s.dto(r), 201


@d.command("approvePolicy")
def approve_policy(request, data, pk):
    d.role(request.user, "ROLE-026")
    d.fresh(request, "policy")
    r = Record.objects.select_for_update().get(pk=data["policy_version_id"], kind="Policy")
    d.require(
        str(r.parent_id or r.id) == str(pk),
        "policy_mismatch",
        "This version belongs to another policy.",
        422,
    )
    d.require(
        r.prepared_by_id != request.user.id,
        "independent_review_required",
        "An independent policy approver is required.",
        403,
    )
    d.require(
        r.status == "draft", "already_reviewed", "This policy version has already been reviewed."
    )
    # Production activation remains deliberately gated by business approval.
    from django.conf import settings

    d.require(
        settings.DEVELOPMENT,
        "activation_not_authorized",
        "Live policy activation requires the approved market configuration.",
        503,
    )
    r.status = "approved" if data["decision"] == "approve" else "rejected"
    r.reviewed_by, r.version = request.user, r.version + 1
    r.save()
    d.emit(request.user, "policy.reviewed", r)
    return s.dto(r), 200


def account_operation(request, op, data, pk):
    d.require(request.user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    if op in ["readPreferences", "changePreference"]:
        r, _ = Record.objects.get_or_create(
            kind="Preferences",
            owner=request.user,
            defaults={"prepared_by": request.user, "data": {}},
        )
        if op == "changePreference":
            r.data.update(data)
            r.version += 1
            r.save()
            d.audit(request.user, "preferences.changed", r)
        return {"version": r.version, **r.data}, 200
    kind = "SavedSearch" if "Search" in op else "SavedVehicle"
    qs = Record.objects.filter(owner=request.user, kind=kind)
    if op in ["listSavedVehicles", "listSavedSearches"]:
        return {"items": [s.dto(r) for r in qs.order_by("-created_at")[:50]]}, 200
    if op == "deleteSavedSearch":
        qs.filter(pk=pk).delete()
        return {}, 200
    d.require(qs.count() < 50, "saved_limit", "Remove a saved item before adding another.")
    r = Record.objects.create(
        kind=kind, owner=request.user, prepared_by=request.user, status="active", data=data
    )
    d.audit(request.user, op, r)
    return s.dto(r), 201


OPERATIONS = {
    "submitDealerApplication": dealer_application,
    "createPaymentObligation": create_obligation,
    "submitPaymentEvidence": payment_evidence,
    "prepareReconciliation": prepare_reconciliation,
    "verifyOwnershipTransfer": verify_transfer,
    "closeTransaction": close_transaction,
    "actOnContent": content_action,
    "reviseContent": revise_content,
    "createPolicyVersion": create_policy,
    "approvePolicy": approve_policy,
    "recordSignatureEvidence": signature,
    "recordDeliveryHandover": handover,
    "createConsumerOffer": consumer_offer,
    "acceptConsumerOffer": accept_offer,
    "decideDealerVerification": dealer_decision,
    "createDealerVerification": create_verification,
    "withdrawConsumerOffer": withdraw_offer,
    "actOnProcurement": procurement_action,
    "actOnCampaign": campaign_action,
}
