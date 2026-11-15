import time
from uuid import uuid4
from django.test import TransactionTestCase, override_settings
from marketplace.models import Obligation, PaymentEvidence, Record, Result, TransactionCase
from . import test_core as core


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class FinanceTests(TransactionTestCase):
    user = core.CoreWorkflowTests.user
    client_for = core.CoreWorkflowTests.client_for
    post = core.CoreWorkflowTests.post

    def setUp(self):
        core.CoreWorkflowTests.setUp(self)
        result = Result.objects.create(
            auction=self.auction, status="pending_seller_decision", seller_decision="accept"
        )
        self.case = TransactionCase.objects.create(
            result=result,
            branch=self.branch,
            vehicle=self.vehicle,
            seller=self.seller,
            buyer=self.dealer,
        )
        self.finance = self.user("finance", ["ROLE-013"])
        self.approver = self.user("approver", ["ROLE-014"])
        self.legal = self.user("legal", ["ROLE-012"])
        self.branch.employees.add(self.finance, self.approver, self.legal)
        self.file = Record.objects.create(
            kind="File",
            owner=self.finance,
            prepared_by=self.finance,
            status="clean",
            data={"case_id": str(self.case.id)},
        )
        self.obligation = Obligation.objects.create(
            transaction=self.case,
            amount_minor=10000,
            currency="EUR",
            prepared_by=self.finance,
            data={"payer_party_id": str(self.dealer.id), "payee_party_id": str(self.seller.id)},
        )

    def elevated(self, user, purpose):
        c = self.client_for(user)
        session = c.session
        session["step_up"] = {"purpose": purpose, "expires": time.time() + 300}
        session.save()
        return c

    def reconciliation(self, amount=10000):
        evidence = PaymentEvidence.objects.create(
            obligation=self.obligation,
            amount_minor=amount,
            currency="EUR",
            file=self.file,
            source_reference=str(uuid4()),
            prepared_by=self.finance,
        )
        self.obligation.status = "evidence_pending"
        self.obligation.save()
        return Record.objects.create(
            kind="Reconciliation",
            owner=self.finance,
            prepared_by=self.finance,
            branch=self.branch,
            status="prepared",
            data={"obligation_id": str(self.obligation.id), "evidence_ids": [str(evidence.id)]},
        )

    def test_reconciliation_requires_exact_amount_and_independent_approver(self):
        r = self.reconciliation(9999)
        c = self.elevated(self.approver, "finance")
        data = {"reason": "External source checked", "evidence_ids": r.data["evidence_ids"]}
        response = self.post(c, f"/reconciliations/{r.id}/approve", data, version=1)
        self.assertEqual(response.status_code, 409, response.content)
        self.obligation.refresh_from_db()
        self.assertEqual(self.obligation.status, "evidence_pending")

    def test_reconciliation_cannot_self_approve_under_second_role(self):
        r = self.reconciliation()
        self.finance.roles.append("ROLE-014")
        self.finance.save()
        response = self.post(
            self.elevated(self.finance, "finance"),
            f"/reconciliations/{r.id}/approve",
            {"reason": "Review", "evidence_ids": r.data["evidence_ids"]},
            version=1,
        )
        self.assertEqual(response.status_code, 403, response.content)

    def test_reconciliation_is_one_effect_and_does_not_verify_title(self):
        r = self.reconciliation()
        key = str(uuid4())
        c = self.elevated(self.approver, "finance")
        response = self.post(
            c,
            f"/reconciliations/{r.id}/approve",
            {
                "reason": "Source evidence independently matched",
                "evidence_ids": r.data["evidence_ids"],
            },
            key,
            1,
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(
            self.post(
                c,
                f"/reconciliations/{r.id}/approve",
                {
                    "reason": "Source evidence independently matched",
                    "evidence_ids": r.data["evidence_ids"],
                },
                key,
                1,
            ).json(),
            response.json(),
        )
        self.obligation.refresh_from_db()
        self.assertEqual(self.obligation.status, "reconciled")
        self.case.refresh_from_db()
        self.assertFalse(self.case.title_verified)

    def test_closure_blocks_missing_milestones(self):
        response = self.post(
            self.client_for(self.legal),
            f"/transactions/{self.case.id}/closure",
            {
                "reason": "Close",
                "policy_version_id": str(self.policy.id),
                "evidence_ids": [str(self.file.id)],
            },
            version=1,
        )
        self.assertEqual(response.status_code, 409, response.content)

    def test_other_customer_cannot_read_finance(self):
        self.assertEqual(
            self.client_for(self.other).get(f"/v1/obligations/{self.obligation.id}").status_code,
            403,
        )

    def test_payment_evidence_source_cannot_be_duplicated(self):
        c = self.client_for(self.finance)
        data = {
            "evidence_id": str(self.file.id),
            "amount_minor": 10000,
            "currency": "EUR",
            "external_reference": "same-source",
            "payer_party_id": str(self.dealer.id),
            "payee_party_id": str(self.seller.id),
        }
        r = self.post(c, f"/obligations/{self.obligation.id}/evidence", data, version=1)
        self.assertIn(r.status_code, [201, 202], r.content)
        self.obligation.refresh_from_db()
        self.obligation.status = "disputed"
        self.obligation.save()
        r = self.post(c, f"/obligations/{self.obligation.id}/evidence", data, version=2)
        self.assertEqual(r.status_code, 409, r.content)
        self.assertEqual(PaymentEvidence.objects.count(), 1)
