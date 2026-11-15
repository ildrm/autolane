import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from uuid import uuid4
from django.db import close_old_connections
from django.test import Client, TransactionTestCase, override_settings
from django.utils import timezone
import pyotp
from marketplace.models import (
    Appointment,
    Auction,
    Audit,
    Bid,
    Branch,
    Inspection,
    Lead,
    Membership,
    Organization,
    Outbox,
    Record,
    Result,
    Revision,
    Slot,
    Taxonomy,
    User,
    Vehicle,
)


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class CoreWorkflowTests(TransactionTestCase):
    """Real PostgreSQL transactions, including competing connection tests."""

    def setUp(self):
        self.seller = self.user("seller", ["ROLE-002", "ROLE-003"])
        self.other = self.user("other", ["ROLE-002"])
        self.dealer = self.user("dealer", ["ROLE-004"])
        self.dealer2 = self.user("dealer2", ["ROLE-004"])
        self.crm = self.user("crm", ["ROLE-011"])
        self.operator = self.user("auction", ["ROLE-010"])
        self.inspector = self.user("inspector", ["ROLE-007"])
        self.reviewer = self.user("reviewer", ["ROLE-008"])
        self.coordinator = self.user("branch", ["ROLE-006"])
        self.branch = Branch.objects.create(
            name="Test Studio", slug="test", city="Test", address="Test"
        )
        self.branch.employees.add(self.operator, self.inspector, self.reviewer, self.coordinator)
        make = Taxonomy.objects.create(name="Example", kind="make")
        model = Taxonomy.objects.create(name="One", kind="model", parent=make)
        self.vehicle = Vehicle.objects.create(
            make=make, model=model, owner=self.seller, year=2022, mileage=100
        )
        self.lead = Lead.objects.create(
            owner=self.seller, assigned_to=self.crm, vehicle=self.vehicle, status="eligible"
        )
        self.slot = Slot.objects.create(
            branch=self.branch,
            starts_at=timezone.now() + timedelta(days=1),
            ends_at=timezone.now() + timedelta(days=1, hours=1),
            capacity=1,
        )
        self.point = str(uuid4())
        self.template = Record.objects.create(
            kind="InspectionTemplate",
            owner=self.reviewer,
            prepared_by=self.reviewer,
            status="approved",
            data={
                "jurisdiction": "EXAMPLE",
                "points": [
                    {
                        "id": self.point,
                        "required": True,
                        "allowed_results": ["pass", "defect", "unknown", "not_applicable"],
                        "evidence_required_on_defect": True,
                    }
                ],
            },
        )
        self.inspection = Inspection.objects.create(
            vehicle=self.vehicle,
            branch=self.branch,
            inspector=self.inspector,
            template=self.template,
            status="published",
        )
        self.revision = Revision.objects.create(
            inspection=self.inspection,
            number=1,
            author=self.inspector,
            reviewer=self.reviewer,
            status="published",
            findings=[{"point_id": self.point, "result": "pass"}],
            checksum="a" * 64,
        )
        self.policy = Record.objects.create(
            kind="Policy",
            owner=self.operator,
            prepared_by=self.operator,
            status="approved",
            data={"content": {"currency": "EUR", "starting_minor": 10000, "increment_minor": 100}},
        )
        self.auction = Auction.objects.create(
            vehicle=self.vehicle,
            report=self.revision,
            policy=self.policy,
            status="open",
            starts_at=timezone.now() - timedelta(hours=1),
            closes_at=timezone.now() + timedelta(hours=1),
            offer_expires_at=timezone.now() + timedelta(days=1),
            currency="EUR",
            starting_minor=10000,
            increment_minor=100,
        )
        for user in [self.dealer, self.dealer2]:
            org = Organization.objects.create(
                legal_name=user.username,
                jurisdiction="EXAMPLE",
                registration_number=user.username,
                status="active",
            )
            Membership.objects.create(user=user, organization=org, can_bid=True)

    def user(self, name, roles):
        return User.objects.create_user(
            username=name + "@example.test",
            email=name + "@example.test",
            password="Development-only-2026!",
            roles=roles,
            contact_verified=True,
        )

    def client_for(self, user):
        c = Client()
        c.force_login(user)
        session = c.session
        session["authenticated_at"] = time.time()
        session["security_epoch"] = user.security_epoch
        session.save()
        return c

    def post(self, c, path, data, key=None, version=None):
        headers = {"HTTP_IDEMPOTENCY_KEY": key or str(uuid4())}
        if version is not None:
            headers["HTTP_IF_MATCH"] = '"' + str(version) + '"'
        return c.post("/v1" + path, json.dumps(data), content_type="application/json", **headers)

    def test_bid_is_durable_and_replay_is_one_effect(self):
        c = self.client_for(self.dealer)
        key = str(uuid4())
        path = f"/auctions/{self.auction.id}/bids"
        first = self.post(c, path, {"amount_minor": 10000, "currency": "EUR"}, key)
        self.assertEqual(first.status_code, 201, first.content)
        again = self.post(c, path, {"amount_minor": 10000, "currency": "EUR"}, key)
        self.assertEqual(first.json(), again.json())
        self.assertEqual(Bid.objects.count(), 1)
        self.assertEqual(Outbox.objects.filter(event_type="auction.bid_accepted").count(), 1)
        conflict = self.post(c, path, {"amount_minor": 10100, "currency": "EUR"}, key)
        self.assertEqual(conflict.status_code, 409)

    def test_replay_checks_revoked_dealer(self):
        c = self.client_for(self.dealer)
        key = str(uuid4())
        path = f"/auctions/{self.auction.id}/bids"
        data = {"amount_minor": 10000, "currency": "EUR"}
        self.assertEqual(self.post(c, path, data, key).status_code, 201)
        Organization.objects.filter(membership__user=self.dealer).update(status="suspended")
        self.assertEqual(self.post(c, path, data, key).status_code, 403)
        self.assertEqual(Bid.objects.count(), 1)

    def test_two_simultaneous_equal_bids_have_one_winner(self):
        clients = [self.client_for(u) for u in [self.dealer, self.dealer2]]

        def compete(client):
            close_old_connections()
            try:
                return self.post(
                    client,
                    f"/auctions/{self.auction.id}/bids",
                    {"amount_minor": 10000, "currency": "EUR"},
                ).status_code
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = list(pool.map(compete, clients))
        self.assertEqual(sorted(statuses), [201, 409])
        self.auction.refresh_from_db()
        self.assertEqual(self.auction.sequence, 1)

    def test_no_bid_after_deadline(self):
        self.auction.closes_at = timezone.now() - timedelta(seconds=1)
        self.auction.save()
        r = self.post(
            self.client_for(self.dealer),
            f"/auctions/{self.auction.id}/bids",
            {"amount_minor": 10000, "currency": "EUR"},
        )
        self.assertEqual(r.status_code, 409)
        self.assertEqual(Bid.objects.count(), 0)

    def test_wrong_currency_fraction_and_increment(self):
        c = self.client_for(self.dealer)
        for data, code in [
            ({"amount_minor": 10000, "currency": "USD"}, 422),
            ({"amount_minor": 10000.5, "currency": "EUR"}, 422),
            ({"amount_minor": 10001, "currency": "EUR"}, 409),
        ]:
            self.assertEqual(
                self.post(c, f"/auctions/{self.auction.id}/bids", data).status_code, code
            )
        self.assertEqual(Bid.objects.count(), 0)

    def test_booking_last_slot_and_wrong_owner(self):
        c = self.client_for(self.seller)
        data = {
            "lead_id": str(self.lead.id),
            "slot_id": str(self.slot.id),
            "branch_id": str(self.branch.id),
        }
        r = self.post(c, "/appointments", data)
        self.assertEqual(r.status_code, 201, r.content)
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.reserved, 1)
        r = self.post(self.client_for(self.other), "/appointments", data)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_booking_conflict_releases_no_extra_capacity(self):
        c = self.client_for(self.seller)
        data = {
            "lead_id": str(self.lead.id),
            "slot_id": str(self.slot.id),
            "branch_id": str(self.branch.id),
        }
        self.assertEqual(self.post(c, "/appointments", data).status_code, 201)
        self.assertEqual(self.post(c, "/appointments", data).status_code, 409)
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.reserved, 1)

    def test_reschedule_stale_and_cancel_exactly_once(self):
        a = Appointment.objects.create(lead=self.lead, slot=self.slot)
        self.slot.reserved = 1
        self.slot.save()
        c = self.client_for(self.seller)
        path = f"/appointments/{a.id}/transitions"
        data = {"action": "cancel", "reason": "Customer request"}
        key = str(uuid4())
        self.assertEqual(self.post(c, path, data, version=999).status_code, 412)
        r = self.post(c, path, data, key, 1)
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(self.post(c, path, data, key, 1).status_code, 200)
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.reserved, 0)

    def test_inspection_draft_submission_and_independent_publication(self):
        self.inspection.status = "draft"
        self.inspection.save()
        Auction.objects.all().delete()
        Revision.objects.all().delete()
        c = self.client_for(self.inspector)
        path = f"/inspections/{self.inspection.id}"
        bad = self.post(
            c,
            path + "/revisions",
            {
                "template_version_id": str(self.template.id),
                "findings": [{"point_id": self.point, "result": "unknown"}],
            },
            version=1,
        )
        self.assertEqual(bad.status_code, 422)
        created = self.post(
            c,
            path + "/revisions",
            {
                "template_version_id": str(self.template.id),
                "findings": [{"point_id": self.point, "result": "pass"}],
            },
            version=1,
        )
        self.assertEqual(created.status_code, 201, created.content)
        submit = self.post(
            c,
            path + "/transitions",
            {
                "action": "submit",
                "reason": "Checklist complete",
                "revision_id": created.json()["id"],
            },
            version=2,
        )
        self.assertEqual(submit.status_code, 200, submit.content)
        self.inspector.roles.append("ROLE-008")
        self.inspector.save()
        denied = self.post(c, path + "/publish", {"revision_id": created.json()["id"]}, version=3)
        self.assertEqual(denied.status_code, 403)
        published = self.post(
            self.client_for(self.reviewer),
            path + "/publish",
            {"revision_id": created.json()["id"]},
            version=3,
        )
        self.assertEqual(published.status_code, 200, published.content)

    def test_material_report_correction_blocks_bid(self):
        response = self.post(
            self.client_for(self.reviewer),
            f"/inspections/{self.inspection.id}/transitions",
            {
                "action": "correct",
                "reason": "Material finding was omitted",
                "revision_id": str(self.revision.id),
            },
            version=1,
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.auction.refresh_from_db()
        self.assertTrue(self.auction.safety_hold)
        self.assertEqual(
            self.post(
                self.client_for(self.dealer),
                f"/auctions/{self.auction.id}/bids",
                {"amount_minor": 10000, "currency": "EUR"},
            ).status_code,
            409,
        )
        self.revision.refresh_from_db()
        self.assertEqual(self.revision.status, "published")

    def test_close_and_seller_acceptance_produce_one_case(self):
        self.assertEqual(
            self.post(
                self.client_for(self.dealer),
                f"/auctions/{self.auction.id}/bids",
                {"amount_minor": 10000, "currency": "EUR"},
            ).status_code,
            201,
        )
        self.auction.refresh_from_db()
        self.auction.closes_at = timezone.now() - timedelta(seconds=1)
        self.auction.save()
        close = self.post(
            self.client_for(self.operator),
            f"/auctions/{self.auction.id}/close",
            {},
            version=self.auction.version,
        )
        self.assertEqual(close.status_code, 200, close.content)
        self.assertEqual(Result.objects.count(), 1)
        key = str(uuid4())
        data = {"decision": "accept", "offer_version": 1, "acknowledged": True}
        path = f"/auction-results/{close.json()['id']}/seller-decision"
        r = self.post(self.client_for(self.seller), path, data, key, 1)
        self.assertEqual(r.status_code, 201, r.content)
        again = self.post(self.client_for(self.seller), path, data, key, 1)
        self.assertEqual(again.json(), r.json())
        from marketplace.models import TransactionCase

        self.assertEqual(TransactionCase.objects.count(), 1)
        self.assertFalse(TransactionCase.objects.get().title_verified)

    def test_session_mfa_requires_valid_proof(self):
        self.reviewer.totp_secret = pyotp.random_base32()
        self.reviewer.save()
        c = Client()
        r = c.post(
            "/v1/auth/login",
            json.dumps({"username": self.reviewer.username, "password": "Development-only-2026!"}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 202, r.content)
        self.assertEqual(c.get("/v1/workspace").status_code, 401)
        r = c.post(
            "/v1/auth/challenges/complete",
            json.dumps(
                {
                    "challenge_id": r.json()["challenge_id"],
                    "method": "totp",
                    "response": pyotp.TOTP(self.reviewer.totp_secret).now(),
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(c.get("/v1/workspace").status_code, 200)

    def test_private_data_and_admin_are_denied(self):
        c = self.client_for(self.other)
        self.assertEqual(c.get(f"/v1/seller-leads/{self.lead.id}").status_code, 404)
        self.assertEqual(c.get("/v1/workspace/audit").status_code, 403)
        self.assertEqual(c.get("/v1/workspace/users").status_code, 403)

    def test_csrf_is_enforced_on_login_and_registration(self):
        c = Client(enforce_csrf_checks=True)
        self.assertEqual(
            c.post(
                "/v1/auth/login",
                json.dumps(
                    {"username": self.seller.username, "password": "Development-only-2026!"}
                ),
                content_type="application/json",
            ).status_code,
            403,
        )
        self.assertEqual(
            c.post("/v1/auth/register", "{}", content_type="application/json").status_code, 403
        )

    def test_dealer_can_read_only_checklists_linked_to_published_eligible_reports(self):
        c = self.client_for(self.dealer)
        self.assertEqual(c.get(f"/v1/inspection-templates/{self.template.id}").status_code, 200)
        unrelated = Record.objects.create(
            kind="InspectionTemplate",
            owner=self.reviewer,
            prepared_by=self.reviewer,
            status="approved",
            data=self.template.data,
        )
        self.assertEqual(c.get(f"/v1/inspection-templates/{unrelated.id}").status_code, 404)

    def test_invalid_json_has_a_stable_client_error(self):
        c = self.client_for(self.seller)
        self.assertEqual(
            c.post("/v1/seller-leads", "{broken", content_type="application/json").status_code, 400
        )
        self.assertEqual(
            c.post("/v1/seller-leads", "[]", content_type="application/json").status_code, 400
        )

    def test_invalid_bearer_does_not_fall_back_to_anonymous(self):
        response = self.client_for(self.seller).get(
            "/v1/vehicle-taxonomy", HTTP_AUTHORIZATION="Bearer invalid"
        )
        self.assertEqual(response.status_code, 401)

    def test_audit_and_outbox_rollback_on_invalid_bid(self):
        before = Audit.objects.count()
        self.post(
            self.client_for(self.dealer),
            f"/auctions/{self.auction.id}/bids",
            {"amount_minor": 1, "currency": "EUR"},
        )
        self.assertEqual(Audit.objects.count(), before)
        self.assertEqual(Outbox.objects.count(), 0)
