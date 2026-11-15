import hashlib
import io
import secrets
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.http import FileResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from PIL import Image, UnidentifiedImageError
from . import domain as d, services as s
from .models import Record
from .permissions import record_access

Image.MAX_IMAGE_PIXELS = 20_000_000


@d.command("createUploadGrant")
def create_grant(request, data, pk=None):
    s.authorize_object(request.user, data["case_id"])
    token = secrets.token_urlsafe(32)
    expires = timezone.now() + timedelta(minutes=5)
    r = Record.objects.create(
        kind="File",
        owner=request.user,
        prepared_by=request.user,
        status="awaiting_upload",
        data={
            **data,
            "grant_hash": hashlib.sha256(token.encode()).hexdigest(),
            "expires_at": expires.isoformat(),
        },
    )
    d.audit(request.user, "file.upload_granted", r)
    return {
        "file_id": str(r.id),
        "upload_url": f"http://127.0.0.1:3000/v1/file-upload/{r.id}?token={token}",
        "expires_at": expires.isoformat().replace("+00:00", "Z"),
        "max_bytes": data["size_bytes"],
    }, 201


def upload(request, pk):
    d.require(request.method == "PUT", "method_not_allowed", "Use PUT to upload bytes.", 405)
    d.require(
        request.user.is_authenticated, "authentication_required", "Sign in to upload evidence.", 401
    )
    d.require(
        0 < int(request.headers.get("Content-Length", "0")) <= 20971520,
        "file_too_large",
        "Maximum file size is 20 MiB.",
        413,
    )
    raw = request.body
    with transaction.atomic():
        r = Record.objects.select_for_update().get(pk=pk, kind="File")
        d.own(request.user, r.owner_id)
        supplied = hashlib.sha256(request.GET.get("token", "").encode()).hexdigest()
        d.require(
            secrets.compare_digest(supplied, r.data.get("grant_hash", ""))
            and parse_datetime(r.data["expires_at"]) > timezone.now()
            and r.status == "awaiting_upload",
            "grant_expired",
            "This upload grant is used or expired.",
            403,
        )
        s.authorize_object(request.user, r.data["case_id"])
        d.require(
            len(raw) == r.data["size_bytes"]
            and hashlib.sha256(raw).hexdigest() == r.data["checksum_sha256"],
            "file_mismatch",
            "Uploaded bytes differ from the declared file.",
            422,
        )
        root = Path(settings.MEDIA_ROOT)
        root.mkdir(parents=True, exist_ok=True)
        original = root / (str(r.id) + ".quarantine")
        original.write_bytes(raw)
        original.chmod(0o600)
        r.status = "scanning"
        # Raster evidence is decoded and re-encoded; only the inert generated derivative can be downloaded.
        if r.data["mime_type"] in ["image/png", "image/jpeg"]:
            try:
                with Image.open(io.BytesIO(raw)) as image:
                    d.require(
                        image.format in ["PNG", "JPEG"],
                        "unsupported_file",
                        "The file format does not match an allowed raster image.",
                        422,
                    )
                    image.load()
                    generated = root / (str(r.id) + ".png")
                    image.convert("RGB").save(generated, format="PNG", optimize=False)
                    generated.chmod(0o600)
                    r.data.update(
                        storage_path=str(generated),
                        derivative_type="image/png",
                        processing="decoded_and_reencoded_raster",
                        original_checksum=r.data["checksum_sha256"],
                    )
                    r.status = "clean"
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
                r.status = "rejected"
        # PDF files remain quarantined until a configured malware/CDR adapter processes them.
        r.data.pop("grant_hash", None)
        r.version += 1
        r.save()
        d.audit(request.user, "file.upload_processed", r)
    return {"id": str(r.id), "status": r.status, "version": r.version}, 200


@d.command("createDownloadGrant")
def download_grant(request, data, pk):
    r = Record.objects.get(pk=pk, kind="File")
    record_access(request.user, r)
    d.require(r.status == "clean", "file_not_ready", "This file is not ready for retrieval.")
    from django.core import signing

    token = signing.dumps({"file": str(r.id), "actor": str(request.user.id)}, salt="file-download")
    expires = timezone.now() + timedelta(seconds=60)
    return {
        "url": f"http://127.0.0.1:3000/v1/file-download/{r.id}?token={token}",
        "expires_at": expires.isoformat().replace("+00:00", "Z"),
    }, 201


def download(request, pk):
    from django.core import signing

    d.require(
        request.user.is_authenticated,
        "authentication_required",
        "Sign in to retrieve evidence.",
        401,
    )
    try:
        proof = signing.loads(request.GET.get("token", ""), salt="file-download", max_age=60)
    except signing.BadSignature:
        raise d.DomainError("grant_expired", "This download grant is invalid or expired.", 403)
    d.require(
        proof["actor"] == str(request.user.id) and proof["file"] == str(pk),
        "access_denied",
        "This grant belongs to another session.",
        403,
    )
    r = Record.objects.get(pk=pk, kind="File")
    record_access(request.user, r)
    d.require(r.status == "clean", "file_not_ready", "This evidence is unavailable.")
    d.audit(request.user, "file.downloaded", r)
    return FileResponse(
        open(r.data["storage_path"], "rb"),
        as_attachment=True,
        filename="evidence.png",
        content_type="image/png",
    )
