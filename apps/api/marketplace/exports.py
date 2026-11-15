import csv
import io
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.core import signing
from django.db.models import Count, Sum
from django.http import FileResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from . import domain as d
from .models import Appointment, Auction, Obligation, Record

REPORT_ROLES = {
    "branch_capacity": ["ROLE-006"],
    "auction_audit": ["ROLE-010"],
    "financial_statement": ["ROLE-014"],
    "approved_metrics": ["ROLE-017"],
}


def authorize(user, data):
    d.role(user, *REPORT_ROLES[data["report"]])
    d.branch_scope(user, data["scope_id"])


@d.command("requestExport")
def request_export(request, data, pk=None):
    authorize(request.user, data)
    d.fresh(request, "export")
    start, end = parse_datetime(data["from"]), parse_datetime(data["to"])
    d.require(
        start < end <= timezone.now() and end - start <= timedelta(days=366),
        "invalid_window",
        "Choose a past reporting window of at most366 days.",
        422,
    )
    r = Record.objects.create(
        kind="Export",
        owner=request.user,
        prepared_by=request.user,
        status="queued",
        branch_id=data["scope_id"],
        data=data,
    )
    d.emit(request.user, "export.requested", r, [request.user.id])
    return {"id": str(r.id), "status": r.status, "version": r.version}, 202


def generate_export(pk):
    r = Record.objects.select_for_update().get(pk=pk, kind="Export")
    if r.status == "ready":
        return
    authorize(r.owner, r.data)
    start, end = parse_datetime(r.data["from"]), parse_datetime(r.data["to"])
    branch = r.branch_id
    rows = []
    if r.data["report"] == "branch_capacity":
        from .models import Slot

        rows = [
            [str(s.id), s.starts_at.isoformat(), s.capacity, s.reserved]
            for s in Slot.objects.filter(
                branch_id=branch, starts_at__gte=start, starts_at__lt=end
            ).order_by("starts_at")[:10000]
        ]
        header = ["slot_id", "starts_at_utc", "capacity", "reserved"]
    elif r.data["report"] == "auction_audit":
        rows = [
            [str(a.id), a.status, a.sequence, a.currency, a.current_bid_minor or ""]
            for a in Auction.objects.filter(
                report__inspection__branch_id=branch, created_at__gte=start, created_at__lt=end
            ).order_by("created_at")[:10000]
        ]
        header = ["auction_id", "status", "accepted_bid_count", "currency", "current_bid_minor"]
    elif r.data["report"] == "financial_statement":
        grouped = (
            Obligation.objects.filter(
                transaction__branch_id=branch, created_at__gte=start, created_at__lt=end
            )
            .values("currency", "status")
            .annotate(total=Sum("amount_minor"), count=Count("id"))
        )
        rows = [[v["currency"], v["status"], v["total"], v["count"]] for v in grouped]
        header = ["currency", "obligation_status", "amount_minor", "obligation_count"]
    else:
        q = Appointment.objects.filter(
            slot__branch_id=branch, created_at__gte=start, created_at__lt=end
        )
        grouped = q.values("status").annotate(count=Count("id"))
        rows = [["appointments", v["status"], v["count"]] for v in grouped if v["count"] >= 5]
        header = ["metric", "status", "count_minimum_cohort_5"]

    def safe(value):
        value = str(value)
        return "'" + value if value.startswith(("=", "+", "-", "@", "\t", "\r")) else value

    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(header)
    writer.writerows([[safe(v) for v in row] for row in rows])
    root = Path(settings.BASE_DIR) / ".local" / "exports"
    root.mkdir(parents=True, exist_ok=True)
    path = root / (str(r.id) + ".csv")
    path.write_text(out.getvalue())
    path.chmod(0o600)
    r.status = "ready"
    r.version += 1
    r.data.update(
        storage_path=str(path),
        row_count=len(rows),
        expires_at=(timezone.now() + timedelta(hours=24)).isoformat(),
    )
    r.save()


@d.command("downloadExport")
def grant(request, data, pk):
    r = Record.objects.get(pk=pk, kind="Export")
    d.own(request.user, r.owner_id)
    authorize(request.user, r.data)
    d.fresh(request, "export")
    d.require(
        r.status == "ready" and parse_datetime(r.data["expires_at"]) > timezone.now(),
        "export_unavailable",
        "This export is not ready or has expired.",
    )
    token = signing.dumps({"id": str(r.id), "actor": str(request.user.id)}, salt="export")
    d.audit(request.user, "export.download_granted", r)
    return {
        "url": f"http://127.0.0.1:3000/v1/export-download/{r.id}?token={token}",
        "expires_at": (timezone.now() + timedelta(seconds=60)).isoformat().replace("+00:00", "Z"),
    }, 201


def download(request, pk):
    d.require(
        request.user.is_authenticated,
        "authentication_required",
        "Sign in to download this export.",
        401,
    )
    try:
        proof = signing.loads(request.GET.get("token", ""), salt="export", max_age=60)
    except signing.BadSignature:
        raise d.DomainError("grant_expired", "This export grant is invalid or expired.", 403)
    d.require(
        proof == {"id": str(pk), "actor": str(request.user.id)},
        "access_denied",
        "This export belongs to another account.",
        403,
    )
    r = Record.objects.get(pk=pk, kind="Export")
    d.own(request.user, r.owner_id)
    authorize(request.user, r.data)
    d.require(
        r.status == "ready" and parse_datetime(r.data["expires_at"]) > timezone.now(),
        "export_unavailable",
        "This export has expired.",
    )
    d.audit(request.user, "export.downloaded", r)
    return FileResponse(
        open(r.data["storage_path"], "rb"),
        content_type="text/csv",
        as_attachment=True,
        filename="autolane-report.csv",
    )
