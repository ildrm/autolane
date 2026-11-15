import os
import secrets
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parents[3]
APP_ENV = os.environ.get("APP_ENV", "development")
DEVELOPMENT = APP_ENV == "development"
DEBUG = os.environ.get("DJANGO_DEBUG") == "1"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEVELOPMENT:
        raise RuntimeError("DJANGO_SECRET_KEY is required outside development")
    secret_file = BASE_DIR / ".local" / "django-secret"
    secret_file.parent.mkdir(exist_ok=True)
    if not secret_file.exists():
        secret_file.write_text(secrets.token_urlsafe(64))
        secret_file.chmod(0o600)
    SECRET_KEY = secret_file.read_text().strip()
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "rest_framework",
    "marketplace",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "marketplace.middleware.SessionPolicyMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
db = urlparse(
    os.environ.get("DATABASE_URL", "postgresql://autolane:autolane-local@127.0.0.1:55432/autolane")
)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db.path.lstrip("/"),
        "USER": db.username,
        "PASSWORD": db.password,
        "HOST": db.hostname,
        "PORT": db.port or 5432,
        "CONN_MAX_AGE": 0,
        "OPTIONS": {"connect_timeout": 5},
    }
}
AUTH_USER_MODEL = "marketplace.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / ".local" / "static"
MEDIA_ROOT = BASE_DIR / ".local" / "private-files"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = not DEVELOPMENT
CSRF_COOKIE_SECURE = not DEVELOPMENT
CSRF_TRUSTED_ORIGINS = [os.environ.get("WEB_ORIGIN", "http://localhost:3000")]
if DEVELOPMENT:
    CSRF_TRUSTED_ORIGINS += ["http://127.0.0.1:3000", "http://localhost:3000"]
CSRF_FAILURE_VIEW = "marketplace.views.csrf_failure"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
if not DEVELOPMENT:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    if os.environ.get("PROVIDER_MODE", "disabled") == "sandbox":
        raise RuntimeError("Sandbox providers cannot run outside development")
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}
EMAIL_BACKEND = (
    "django.core.mail.backends.filebased.EmailBackend"
    if DEVELOPMENT
    else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_FILE_PATH = BASE_DIR / ".local" / "mail"
DEFAULT_FROM_EMAIL = "Autolane <no-reply@localhost>"

DATA_UPLOAD_MAX_MEMORY_SIZE = 21 * 1024 * 1024
