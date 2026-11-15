import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from marketplace.domain import close_locked, emit
from marketplace.models import Auction, Notification, Outbox


def tick():
    with transaction.atomic():
        for a in Auction.objects.select_for_update(skip_locked=True).filter(
            status="scheduled",
            starts_at__lte=timezone.now(),
            closes_at__gt=timezone.now(),
            safety_hold=False,
        )[:10]:
            if a.report.status == "published" and a.policy.status == "approved":
                a.status = "open"
                a.version += 1
                a.save()
                emit(None, "auction.opened", a)
        for a in Auction.objects.select_for_update(skip_locked=True).filter(
            status__in=["open", "paused"], closes_at__lte=timezone.now()
        )[:10]:
            close_locked(None, a)

    ids = list(
        Outbox.objects.filter(status="pending", available_at__lte=timezone.now())
        .order_by("created_at")
        .values_list("pk", flat=True)[:20]
    )
    for pk in ids:
        with transaction.atomic():
            event = (
                Outbox.objects.select_for_update(skip_locked=True)
                .filter(pk=pk, status="pending")
                .first()
            )
            if event is None:
                continue
            try:
                with transaction.atomic():
                    if event.event_type == "export.requested":
                        from marketplace.exports import generate_export

                        generate_export(event.aggregate_id)
                    for uid in event.payload.get("recipients", []):
                        Notification.objects.get_or_create(
                            recipient_id=uid,
                            event=event,
                            defaults={
                                "subject": event.event_type.replace(".", " ")
                                .replace("_", " ")
                                .capitalize(),
                                "body": "Your case has an update. Open your dashboard to review the authoritative status.",
                            },
                        )
                event.status = "delivered"
            except Exception:
                event.attempts += 1
                if event.attempts >= 5:
                    event.status = "dead_letter"
                    if event.event_type == "export.requested":
                        from marketplace.models import Record

                        Record.objects.filter(pk=event.aggregate_id, kind="Export").update(
                            status="failed"
                        )
                else:
                    from datetime import timedelta

                    event.available_at = timezone.now() + timedelta(
                        seconds=[1, 5, 30, 120, 600][event.attempts - 1]
                    )
                import logging

                logging.getLogger(__name__).exception(
                    "Outbox processing failed; event type=%s attempt=%d",
                    event.event_type,
                    event.attempts,
                )
            event.save(update_fields=["status", "attempts", "available_at"])


class Command(BaseCommand):
    help = (
        "Process durable in-app notifications and auction deadlines with one low-frequency worker."
    )

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true")

    def handle(self, **options):
        while True:
            tick()
            if options["once"]:
                break
            time.sleep(5)
