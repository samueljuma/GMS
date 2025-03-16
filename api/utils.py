from rest_framework.response import Response
from rest_framework.views import exception_handler


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
def extract_error_details(data):
    """
    Extracts meaningful error messages from various DRF exceptions dynamically.
    - Supports different error structures (dict, list, string).
    """
    if isinstance(data, dict):
        # Extract 'detail' if available, otherwise join all error messages
        return data.get("detail") or "; ".join(
            f"{key}: {', '.join(map(str, value))}" if isinstance(value, list) else f"{key}: {value}"
            for key, value in data.items()
        )
    elif isinstance(data, list):
        return "; ".join(map(str, data))  # Convert list errors into readable text
    return str(data)  # Convert raw strings or other types to string

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def custom_exception_handler(exc, context):
    """
    Custom exception handler to standardize error responses.
    - Uses DRF's built-in `exception_handler` for proper response handling.
    - Enhances error structure for better readability.
    """
    response = exception_handler(exc, context)

    # Define base error response
    error_response = {
        "message": "An error occurred",
        "error": "Internal Server Error",
    }

    if response is not None:
        error_response["message"] = extract_error_details(response.data)
        error_response["error"] = response.data.get("error", exc.__class__.__name__.replace("_", " ").title())

        # Ensure response returns a structured error
        response.data = error_response
    else:
        # If DRF didn't handle it, return a fallback 500 error response
        error_response["message"] = str(exc)
        response = Response(error_response, status=500)

    return response

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
