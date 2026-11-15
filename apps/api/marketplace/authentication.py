import secrets
import time
from datetime import timedelta
import pyotp
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.db import transaction
from django.middleware.csrf import get_token, rotate_token
from django.utils import timezone
from .domain import DomainError, audit, require
from .models import Challenge, RateBucket, User


def throttle(key, limit=10, seconds=300):
    with transaction.atomic():
        bucket, _ = RateBucket.objects.get_or_create(
            key=key, defaults={"expires_at": timezone.now() + timedelta(seconds=seconds)}
        )
        bucket = RateBucket.objects.select_for_update().get(pk=key)
        if bucket.expires_at <= timezone.now():
            bucket.count, bucket.expires_at = 0, timezone.now() + timedelta(seconds=seconds)
        require(bucket.count < limit, "rate_limited", "Too many attempts. Try again later.", 429)
        bucket.count += 1
        bucket.save()


def begin_session(request, data):
    throttle("login:" + request.META.get("REMOTE_ADDR", "local"))
    user = authenticate(
        request, username=data.get("username", "").lower(), password=data.get("password", "")
    )
    require(
        user is not None and user.is_active,
        "invalid_credentials",
        "The sign-in details could not be verified.",
        401,
    )
    require(
        user.contact_verified, "contact_unverified", "Verify your email before signing in.", 403
    )
    staff = any(
        r not in ["ROLE-001", "ROLE-002", "ROLE-003", "ROLE-004", "ROLE-005"] for r in user.roles
    )
    if staff or user.totp_secret:
        require(
            bool(user.totp_secret),
            "mfa_setup_required",
            "Ask your security administrator to enroll your second factor.",
            403,
        )
        request.session.cycle_key()
        challenge = Challenge.objects.create(
            user=user,
            purpose="login",
            secret_hash="totp",
            session_key=request.session.session_key,
            expires_at=timezone.now() + timedelta(minutes=5),
        )
        return {
            "challenge_id": str(challenge.id),
            "expires_at": challenge.expires_at.isoformat().replace("+00:00", "Z"),
            "status": "mfa_required",
        }, 202
    return finish_login(request, user), 200


def finish_login(request, user):
    login(request, user)
    request.session["authenticated_at"] = time.time()
    request.session["security_epoch"] = user.security_epoch
    rotate_token(request)
    audit(user, "auth.login", user)
    return session_dto(request)


def session_dto(request):
    require(request.user.is_authenticated, "authentication_required", "Sign in to continue.", 401)
    return {
        "user_id": str(request.user.id),
        "expires_at": (timezone.now() + timedelta(minutes=30)).isoformat().replace("+00:00", "Z"),
        "mfa_required": False,
        "csrf_token": get_token(request),
    }


def complete_challenge(request, data, purpose="login"):
    # Attempt accounting must persist even when a proof is rejected.
    with transaction.atomic():
        challenge = (
            Challenge.objects.select_for_update()
            .filter(pk=data.get("challenge_id"), purpose=purpose)
            .first()
        )
        require(
            challenge is not None
            and not challenge.consumed
            and challenge.attempts < 5
            and challenge.expires_at > timezone.now()
            and challenge.session_key == request.session.session_key,
            "invalid_challenge",
            "This verification request is invalid or expired.",
            403,
        )
        challenge.attempts += 1
        valid = data.get("method", "totp") == "totp" and pyotp.TOTP(
            challenge.user.totp_secret
        ).verify(str(data.get("response", "")), valid_window=0)
        if valid:
            challenge.consumed = True
        challenge.save()
    require(valid, "invalid_code", "The verification code is invalid.", 403)
    if purpose == "login":
        return finish_login(request, challenge.user), 200
    require(
        request.user.id == challenge.user_id,
        "access_denied",
        "This verification is for a different session.",
        403,
    )
    request.session["step_up"] = {"purpose": challenge.secret_hash, "expires": time.time() + 300}
    return {
        "status": "verified",
        "purpose": challenge.secret_hash,
        "expires_at": (timezone.now() + timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
    }, 200


def start_stepup(request, data):
    require(
        request.user.is_authenticated and request.user.totp_secret,
        "mfa_required",
        "An enrolled second factor is required.",
        403,
    )
    purpose = {
        "finance_approval": "finance",
        "policy_approval": "policy",
        "dealer_suspension": "dealer_risk",
        "access_change": "access",
        "legal_approval": "legal",
        "consumer_offer": "consumer_offer",
        "export_approval": "export",
    }.get(data.get("purpose"))
    require(purpose is not None, "invalid_purpose", "Choose a supported verification purpose.", 422)
    c = Challenge.objects.create(
        user=request.user,
        purpose="stepup",
        secret_hash=purpose,
        session_key=request.session.session_key,
        expires_at=timezone.now() + timedelta(minutes=5),
    )
    return {
        "challenge_id": str(c.id),
        "purpose": purpose,
        "expires_at": c.expires_at.isoformat().replace("+00:00", "Z"),
    }, 202


def register_user(request, data):
    throttle("register:" + request.META.get("REMOTE_ADDR", "local"), 5, 3600)
    from django.core.validators import validate_email

    email = data.get("email", "").strip().lower()
    validate_email(email)
    validate_password(data.get("password", ""))
    # Same response for existing identities; no silent account linking.
    if not User.objects.filter(username=email).exists():
        user = User.objects.create_user(
            username=email,
            email=email,
            password=data["password"],
            first_name=data.get("name", "")[:150],
            roles=["ROLE-002", "ROLE-003"],
        )
        token = secrets.token_urlsafe(32)
        c = Challenge.objects.create(
            user=user,
            purpose="verify",
            secret_hash=make_password(token),
            expires_at=timezone.now() + timedelta(minutes=15),
        )
        send_mail(
            "Verify your Autolane email",
            f"Verify your email using verification ID {c.id} and token {token}.\nThis proof expires in 15 minutes.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
    return {"status": "accepted", "message": "Check your email for the next step."}, 202


def verify_email(data):
    with transaction.atomic():
        c = Challenge.objects.select_for_update().get(pk=data["challenge_id"], purpose="verify")
        require(
            not c.consumed
            and c.expires_at > timezone.now()
            and check_password(data["token"], c.secret_hash),
            "invalid_verification",
            "This verification link is invalid or expired.",
            403,
        )
        c.consumed = True
        c.save()
        c.user.contact_verified = True
        c.user.save(update_fields=["contact_verified"])
    return {"status": "verified"}, 200


def recovery(request, data):
    throttle("recovery:" + request.META.get("REMOTE_ADDR", "local"), 5, 3600)
    user = User.objects.filter(
        email=data.get("email", data.get("identifier", "")).lower(), contact_verified=True
    ).first()
    if user:
        token = secrets.token_urlsafe(32)
        c = Challenge.objects.create(
            user=user,
            purpose="recovery",
            secret_hash=make_password(token),
            expires_at=timezone.now() + timedelta(minutes=15),
        )
        send_mail(
            "Autolane account recovery",
            f"Recovery token: {c.id}:{token}\nIf you did not request this, ignore this email.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
    return {"status": "accepted"}, 202


def complete_recovery(request, data):
    throttle("recover-complete:" + request.META.get("REMOTE_ADDR", "local"))
    try:
        pk, token = data["recovery_token"].split(":", 1)
    except (ValueError, KeyError):
        raise DomainError("invalid_recovery", "This recovery request is invalid or expired.", 403)
    validate_password(data.get("new_password", ""))
    with transaction.atomic():
        c = Challenge.objects.select_for_update().get(pk=pk, purpose="recovery")
        require(
            not c.consumed
            and c.expires_at > timezone.now()
            and check_password(token, c.secret_hash),
            "invalid_recovery",
            "This recovery request is invalid or expired.",
            403,
        )
        c.user.set_password(data["new_password"])
        c.user.security_epoch += 1
        c.user.save()
        Challenge.objects.filter(user=c.user, purpose="recovery").update(consumed=True)
        audit(c.user, "auth.recovery_completed", c.user)
    return {"status": "accepted"}, 200
