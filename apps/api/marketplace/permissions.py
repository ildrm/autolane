from .models import Appointment, Auction, Lead, Membership, Record, Result, Revision
from .domain import branch_scope, own, require, role

DOMAIN_ROLES = {
    "ConsumerOffer": ["ROLE-021", "ROLE-011"],
    "Valuation": ["ROLE-009"],
    "DealerVerification": ["ROLE-019"],
    "VehicleListing": ["ROLE-021"],
    "PurchaseRequest": ["ROLE-011"],
    "ProcurementRequest": ["ROLE-011"],
    "FinancingApplication": ["ROLE-024"],
    "Contract": ["ROLE-012"],
    "ContractTemplate": ["ROLE-012"],
    "OwnershipTransfer": ["ROLE-012"],
    "Reconciliation": ["ROLE-013", "ROLE-014"],
    "Delivery": ["ROLE-020"],
    "WarrantyClaim": ["ROLE-022"],
    "SupportTicket": ["ROLE-011"],
    "Content": ["ROLE-015"],
    "Campaign": ["ROLE-025"],
    "Policy": ["ROLE-016", "ROLE-026"],
    "PrivacyRequest": ["ROLE-023"],
    "InspectionTemplate": ["ROLE-007", "ROLE-008"],
    "File": [],
    "Export": ["ROLE-017"],
}


def case_access(user, case):
    require(user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    if user.id in [case.seller_id, case.buyer_id]:
        return
    if (
        case.organization_id
        and Membership.objects.filter(
            user=user, organization=case.organization, active=True
        ).exists()
    ):
        return
    role(user, "ROLE-012", "ROLE-013", "ROLE-014", "ROLE-020", "ROLE-022")
    require(case.branch_id is not None, "access_denied", "This case has no assigned branch.", 403)
    branch_scope(user, case.branch_id)


def lead_access(user, lead):
    if user.id == lead.owner_id:
        return
    if "ROLE-011" in user.roles:
        own(user, lead.assigned_to_id)
        return
    require(
        bool(set(user.roles) & {"ROLE-006", "ROLE-007", "ROLE-008", "ROLE-010"}),
        "not_found",
        "This record is not available.",
        404,
    )
    branch_ids = Appointment.objects.filter(lead=lead).values_list("slot__branch_id", flat=True)
    require(
        user.branches.filter(id__in=branch_ids).exists(),
        "not_found",
        "This record is not available.",
        404,
    )


def record_access(user, r, write=False):
    require(user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    if not write and r.owner_id == user.id:
        return
    if not write and r.kind == "InspectionTemplate" and "ROLE-004" in user.roles:
        from .domain import eligible_member

        eligible_member(user)
        require(
            r.status == "approved"
            and Auction.objects.filter(
                report__inspection__template=r,
                report__status="published",
                status__in=["scheduled", "open", "paused", "closed"],
            ).exists(),
            "not_found",
            "This checklist is not available.",
            404,
        )
        return
    if r.kind == "File":
        parent = r.data.get("case_id")
        require(bool(parent), "not_found", "This file is not available.", 404)
        from .services import authorize_object

        authorize_object(user, parent)
        return
    roles = DOMAIN_ROLES.get(r.kind, [])
    role(user, *roles)
    if r.branch_id:
        branch_scope(user, r.branch_id)
    elif r.kind not in [
        "Content",
        "Campaign",
        "Policy",
        "PrivacyRequest",
        "InspectionTemplate",
        "ContractTemplate",
        "DealerVerification",
    ]:
        require(
            r.prepared_by_id == user.id or (r.data.get("assigned_to") == str(user.id)),
            "not_found",
            "This record is not assigned to you.",
            404,
        )


def auction_access(user, auction):
    if "ROLE-004" in user.roles:
        from .domain import eligible_member

        eligible_member(user)
        require(
            auction.status in ["scheduled", "open", "paused", "closed"],
            "not_found",
            "This auction is not available.",
            404,
        )
    elif user.id == auction.vehicle.owner_id:
        return
    else:
        role(user, "ROLE-010")
        branch_scope(user, auction.report.inspection.branch_id)


def authorize_replay(request, operation, args, response):
    u = request.user
    creation_roles = {
        "createSellerLead": ["ROLE-002"],
        "createInspection": ["ROLE-006", "ROLE-008"],
        "createAuction": ["ROLE-010"],
        "createPaymentObligation": ["ROLE-013"],
        "prepareReconciliation": ["ROLE-013"],
        "createConsumerOffer": ["ROLE-021", "ROLE-011"],
    }
    if operation == "createOperationalRecord":
        kind = args[0]
        allowed = (
            ["ROLE-002", "ROLE-003", "ROLE-004", "ROLE-011"]
            if kind
            in [
                "SupportTicket",
                "WarrantyClaim",
                "PurchaseRequest",
                "ProcurementRequest",
                "PrivacyRequest",
                "FinancingApplication",
            ]
            else DOMAIN_ROLES.get(kind, [])
        )
        role(u, *allowed)
        if response.get("id"):
            record_access(u, Record.objects.get(pk=response["id"]))
        return
    if operation in creation_roles:
        role(u, *creation_roles[operation])
        if response.get("id"):
            from .services import authorize_object

            authorize_object(u, response["id"])
        return
    if "code" in response:
        if args:
            from .services import authorize_object

            authorize_object(u, str(args[0]))
        return
    if operation == "submitBid":
        from .domain import eligible_member

        role(u, "ROLE-004")
        eligible_member(u)
        auction_access(u, Auction.objects.get(pk=args[0]))
    elif operation in ["createAppointment", "transitionAppointment"]:
        a = Appointment.objects.get(pk=response["id"])
        lead_access(u, a.lead)
    elif operation == "createSellerLead":
        lead_access(u, Lead.objects.get(pk=response["id"]))
    elif operation == "recordSellerDecision":
        own(u, Result.objects.get(pk=args[0]).auction.vehicle.owner_id)
    elif operation in ["createInspectionRevision", "publishInspection"]:
        r = Revision.objects.get(pk=response["id"])
        role(u, "ROLE-007", "ROLE-008")
        branch_scope(u, r.inspection.branch_id)
    elif operation == "closeAuction":
        role(u, "ROLE-010")
        auction_access(u, Auction.objects.get(pk=args[0]))
    elif operation == "approveReconciliation":
        role(u, "ROLE-014")
        record_access(u, Record.objects.get(pk=args[0]), write=True)
    elif args:
        # All remaining binding commands use an explicit scoped aggregate check.
        from .services import authorize_object

        authorize_object(u, str(args[0]))
    else:
        # Creation receipts stay private to their current principal and role family.
        require(
            u.is_active and bool(u.roles),
            "access_denied",
            "This account no longer has access.",
            403,
        )
