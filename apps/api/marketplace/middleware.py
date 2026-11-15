import time
from django.contrib.auth import logout


class SessionPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (
            time.time() - request.session.get("authenticated_at", 0) > 43200
            or request.session.get("security_epoch") != request.user.security_epoch
        ):
            logout(request)
        response = self.get_response(request)
        if request.path.startswith("/v1/"):
            response["Cache-Control"] = "private, no-store"
            response["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        return response
