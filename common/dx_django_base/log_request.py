import logging
from time import perf_counter

from django.conf import settings


class LogRequestMiddleware:
    """Log request."""

    def __init__(self, get_response):
        """Extend as required by Django."""
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        """Log the request/response cycle."""
        path_info = request.path_info
        if path_info.startswith("/__debug__/"):
            return self.get_response(request)

        log_record = {
            "user": request.user.username,
            "method": request.method,
            "scheme": request.scheme,
            "url": path_info,
            "query_string": request.META.get("QUERY_STRING", ""),
            "remote_address": request.META.get("REMOTE_ADDR", ""),
            "remote_host": request.get_host(),
            "forwarded_for": request.headers.get("x-forwarded-for", ""),
            "content_type": request.content_type,
            "referer": request.headers.get("referer", ""),
            "user_agent": request.headers.get("user-agent", ""),
        }
        start = perf_counter()
        response = self.get_response(request)
        log_record["execution_time_ms"] = round((perf_counter() - start), 3) * 1000
        log_record["response_code"] = response.status_code
        api_url = getattr(settings, "API_URL", None)
        if (
            api_url
            and path_info.startswith(settings.API_URL)
            and not request.user.is_anonymous
        ):
            # API user is set after the request is processed
            log_record["user"] = request.user.username

        if 200 <= response.status_code < 400:
            self.logger.info(log_record)
        elif 400 <= response.status_code < 500:
            self.logger.warning(log_record)
        else:
            self.logger.error(log_record)
        return response
