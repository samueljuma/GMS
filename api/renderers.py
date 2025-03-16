from rest_framework.renderers import JSONRenderer
from django.utils.timezone import now
import time

class CustomJSONRenderer(JSONRenderer):
    """
    Custom renderer to ensure a consistent JSON response format.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response", None)
        request = renderer_context.get("request", None)

        path = request.path if request else "N/A"
        method = request.method if request else "N/A"
        timestamp = now().isoformat()
        duration = (
            f"{int((time.time() - request.start_time) * 1000)}ms"
            if hasattr(request, "start_time")
            else "N/A"
        )

        # If response is an error (status_code >= 400)
        if response is not None and response.status_code >= 400:
            return super().render(
                {
                    "status": "Fail",
                    "statusCode": response.status_code,
                    "timestamp": timestamp,
                    "path": path,
                    "message": data.get("message", "An error occurred"),
                    "error": data.get("error", "Error"),
                    "duration": duration,
                }
            )

        # Standard success response format
        return super().render(
            {
                "status": "Success",
                "data": data if data else {},
                "path": path,
                "method": method,
                "timestamp": timestamp,
                "duration": duration,
            }
        )
