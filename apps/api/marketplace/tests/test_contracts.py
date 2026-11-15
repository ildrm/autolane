from django.test import TransactionTestCase, override_settings
from marketplace.contracts import route_match, validator
from . import test_core as core


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class RuntimeContractTests(TransactionTestCase):
    user = core.CoreWorkflowTests.user
    client_for = core.CoreWorkflowTests.client_for
    post = core.CoreWorkflowTests.post

    def setUp(self):
        core.CoreWorkflowTests.setUp(self)

    def assert_contract(self, path, response, method="GET"):
        self.assertLess(response.status_code, 300, response.content)
        op, _ = route_match(path.lstrip("/"), method)
        schema = op["responses"][str(response.status_code)]["content"]["application/json"]["schema"]
        self.assertEqual(list(validator(schema).iter_errors(response.json())), [], response.content)

    def test_public_taxonomy_branch_and_slot_response_contracts(self):
        c = self.client_for(self.seller)
        for path in ["/vehicle-taxonomy", "/branches", f"/branches/{self.branch.id}/slots"]:
            self.assert_contract(path, c.get("/v1" + path))

    def test_authorized_auction_and_accepted_bid_response_contracts(self):
        c = self.client_for(self.dealer)
        path = f"/auctions/{self.auction.id}"
        self.assert_contract(path, c.get("/v1" + path))
        path += "/bids"
        self.assert_contract(
            path, self.post(c, path, {"amount_minor": 10000, "currency": "EUR"}), "POST"
        )

    def test_booking_response_contract(self):
        c = self.client_for(self.seller)
        data = {
            "lead_id": str(self.lead.id),
            "branch_id": str(self.branch.id),
            "slot_id": str(self.slot.id),
        }
        self.assert_contract("/appointments", self.post(c, "/appointments", data), "POST")
