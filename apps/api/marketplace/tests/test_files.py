import hashlib
import io
import tempfile
from urllib.parse import urlparse
from PIL import Image
from django.test import TransactionTestCase, override_settings
from marketplace.models import Record
from . import test_core as core


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class FileTests(TransactionTestCase):
    user = core.CoreWorkflowTests.user
    client_for = core.CoreWorkflowTests.client_for
    post = core.CoreWorkflowTests.post

    def setUp(self):
        core.CoreWorkflowTests.setUp(self)

    def test_private_upload_checks_hash_ownership_and_sanitizes_image(self):
        stream = io.BytesIO()
        Image.new("RGB", (2, 2), (10, 20, 30)).save(stream, format="PNG")
        raw = stream.getvalue()
        c = self.client_for(self.seller)
        grant = self.post(
            c,
            "/files/upload-grants",
            {
                "case_id": str(self.lead.id),
                "kind": "identity",
                "mime_type": "image/png",
                "size_bytes": len(raw),
                "checksum_sha256": hashlib.sha256(raw).hexdigest(),
            },
        )
        self.assertEqual(grant.status_code, 201, grant.content)
        u = urlparse(grant.json()["upload_url"])
        with tempfile.TemporaryDirectory() as storage, override_settings(MEDIA_ROOT=storage):
            response = c.put(u.path + "?" + u.query, raw, content_type="image/png")
            self.assertEqual(response.status_code, 200, response.content)
            self.assertEqual(response.json()["status"], "clean")
            record = Record.objects.get(pk=grant.json()["file_id"])
            self.assertNotIn("grant_hash", record.data)
            self.assertEqual(
                self.client_for(self.other).get("/v1/files/" + str(record.id)).status_code, 404
            )
            self.assertEqual(
                c.put(u.path + "?" + u.query, raw, content_type="image/png").status_code, 403
            )

    def test_unknown_file_bytes_are_not_declared_clean(self):
        raw = b"not a real image"
        c = self.client_for(self.seller)
        grant = self.post(
            c,
            "/files/upload-grants",
            {
                "case_id": str(self.lead.id),
                "kind": "identity",
                "mime_type": "image/png",
                "size_bytes": len(raw),
                "checksum_sha256": hashlib.sha256(raw).hexdigest(),
            },
        )
        self.assertEqual(grant.status_code, 201, grant.content)
        u = urlparse(grant.json()["upload_url"])
        with tempfile.TemporaryDirectory() as storage, override_settings(MEDIA_ROOT=storage):
            response = c.put(u.path + "?" + u.query, raw, content_type="image/png")
            self.assertEqual(response.status_code, 200, response.content)
            self.assertEqual(response.json()["status"], "rejected")
