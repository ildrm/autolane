import tempfile
import time
from datetime import timedelta
from django.db import transaction
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from marketplace.exports import generate_export
from . import test_core as core


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class OperationsTests(TransactionTestCase):
    user = core.CoreWorkflowTests.user
    client_for = core.CoreWorkflowTests.client_for
    post = core.CoreWorkflowTests.post

    def setUp(self):
        core.CoreWorkflowTests.setUp(self)

    def test_export_job_persists_and_requires_current_role_for_download(self):
        c = self.client_for(self.coordinator)
        session = c.session
        session["step_up"] = {"purpose": "export", "expires": time.time() + 300}
        session.save()
        now = timezone.now()
        data = {
            "report": "branch_capacity",
            "from": (now - timedelta(days=2)).isoformat().replace("+00:00", "Z"),
            "to": now.isoformat().replace("+00:00", "Z"),
            "purpose": "Review branch capacity",
            "scope_id": str(self.branch.id),
        }
        response = self.post(c, "/exports", data)
        self.assertEqual(response.status_code, 202, response.content)
        pk = response.json()["id"]
        with tempfile.TemporaryDirectory() as root, override_settings(BASE_DIR=root):
            with transaction.atomic():
                generate_export(pk)
            job = c.get("/v1/exports/" + pk)
            self.assertEqual(job.status_code, 200, job.content)
            self.assertEqual(job.json()["status"], "ready")
            grant = self.post(c, f"/exports/{pk}/download-grants", {})
            self.assertEqual(grant.status_code, 201, grant.content)
            self.coordinator.roles = []
            self.coordinator.save()
            from urllib.parse import urlparse

            url = urlparse(grant.json()["url"])
            self.assertEqual(c.get(url.path + "?" + url.query).status_code, 403)

    def test_customer_cannot_request_operational_export(self):
        now = timezone.now()
        response = self.post(
            self.client_for(self.seller),
            "/exports",
            {
                "report": "branch_capacity",
                "from": (now - timedelta(days=1)).isoformat().replace("+00:00", "Z"),
                "to": now.isoformat().replace("+00:00", "Z"),
                "purpose": "unauthorized export",
                "scope_id": str(self.branch.id),
            },
        )
        self.assertEqual(response.status_code, 403, response.content)

    def test_outbox_delivery_is_idempotent_and_poison_work_is_retried(self):
        from marketplace.models import Outbox, Notification
        from marketplace.management.commands.work_events import tick
        from uuid import uuid4

        event = Outbox.objects.create(
            event_type="seller.updated",
            aggregate_id=self.lead.id,
            aggregate_version=1,
            payload={"recipients": [str(self.seller.id)]},
            available_at=timezone.now(),
        )
        tick()
        tick()
        self.assertEqual(Notification.objects.filter(event=event).count(), 1)
        poison = Outbox.objects.create(
            event_type="export.requested",
            aggregate_id=uuid4(),
            aggregate_version=1,
            payload={},
            available_at=timezone.now(),
        )
        with self.assertLogs("marketplace.management.commands.work_events", level="ERROR"):
            tick()
        poison.refresh_from_db()
        self.assertEqual(poison.attempts, 1)
        self.assertEqual(poison.status, "pending")
        self.assertGreater(poison.available_at, timezone.now())

    def test_content_publication_requires_independent_revision_approval(self):
        editor = self.user("editor", ["ROLE-015"])
        reviewer = self.user("publisher", ["ROLE-015"])
        now = timezone.now()
        content = {
            "slug": "test-guide",
            "title": "A considered car buying guide",
            "blocks": [{"kind": "paragraph", "text": "Review real condition evidence."}],
            "source_urls": [],
            "review_at": (now + timedelta(days=10)).isoformat().replace("+00:00", "Z"),
            "indexable": True,
            "canonical_path": "/journal/test-guide",
        }
        c = self.client_for(editor)
        r = self.post(c, "/content-items", content)
        self.assertEqual(r.status_code, 201, r.content)
        pk = r.json()["id"]
        revision = r.json()["revision_id"]
        action = {
            "action": "submit_review",
            "revision_id": revision,
            "reason": "Ready for editorial review",
        }
        self.assertEqual(
            self.post(c, f"/content-items/{pk}/actions", action, version=1).status_code, 200
        )
        action["action"] = "approve"
        self.assertEqual(
            self.post(c, f"/content-items/{pk}/actions", action, version=2).status_code, 403
        )
        self.assertEqual(
            self.post(
                self.client_for(reviewer), f"/content-items/{pk}/actions", action, version=2
            ).status_code,
            200,
        )
        action["action"] = "publish"
        self.assertEqual(
            self.post(c, f"/content-items/{pk}/actions", action, version=3).status_code, 200
        )
        public = self.client_for(self.other).get("/v1/published-content/test-guide")
        self.assertEqual(public.status_code, 200, public.content)
        self.assertEqual(public.json()["title"], content["title"])
