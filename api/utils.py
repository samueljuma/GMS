from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException, ValidationError, ParseError, AuthenticationFailed, NotAuthenticated, 
    PermissionDenied, NotFound, MethodNotAllowed, NotAcceptable, UnsupportedMediaType, Throttled
)
from django.utils.timezone import now

def format_validation_errors(errors):
    """
    Converts DRF validation errors into a single readable error message.
    """
    if isinstance(errors, list):
        return " ; ".join(errors)
    
    if isinstance(errors, dict):
        return " ; ".join([f"{key}: {', '.join(value)}" for key, value in errors.items()])
    
    return str(errors)

def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler to standardize error responses.
    """
    # Call DRF's default exception handler
    response = exception_handler(exc, context)

    # Extract request details
    request = context.get("request", None)
    path = request.path if request else "N/A"

    # Default error response structure
    error_response = {
        "statusCode": response.status_code if response else 500,
        "timestamp": now().isoformat(),
        "path": path,
        "message": "An error occurred",
        "error": "Internal Server Error",
    }

    if isinstance(exc, ValidationError):
        error_response["message"] = format_validation_errors(exc.detail)
        error_response["error"] = "Validation Error"

    elif isinstance(exc, ParseError):
        error_response["message"] = "Malformed request syntax or JSON parse error"
        error_response["error"] = "Bad Request"

    elif isinstance(exc, AuthenticationFailed):
        error_response["message"] = str(exc.detail)
        error_response["error"] = "Unauthorized"

    elif isinstance(exc, NotAuthenticated):
        error_response["message"] = "Authentication credentials were not provided"
        error_response["error"] = "Unauthorized"

    elif isinstance(exc, PermissionDenied):
        error_response["message"] = str(exc.detail)
        error_response["error"] = "Forbidden"

    elif isinstance(exc, NotFound):
        error_response["message"] = str(exc.detail)
        error_response["error"] = "Not Found"

    elif isinstance(exc, MethodNotAllowed):
        error_response["message"] = f"Method '{request.method}' is not allowed on this endpoint"
        error_response["error"] = "Method Not Allowed"

    elif isinstance(exc, NotAcceptable):
        error_response["message"] = str(exc.detail)
        error_response["error"] = "Not Acceptable"

    elif isinstance(exc, UnsupportedMediaType):
        error_response["message"] = f"Unsupported media type: {request.content_type}"
        error_response["error"] = "Unsupported Media Type"

    elif isinstance(exc, Throttled):
        error_response["message"] = f"Request was throttled. Try again in {exc.wait} seconds"
        error_response["error"] = "Too Many Requests"

    elif isinstance(exc, APIException):
        error_response["message"] = str(exc.detail)
        error_response["error"] = exc.default_code.replace("_", " ").title()

    # Update response data if DRF handled the exception
    if response is not None:
        response.data = error_response
    else:
        # Fallback response if DRF didn't handle the exception
        response = Response(error_response, status=500)

    return response
