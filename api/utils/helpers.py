import uuid
import time


def generate_reference(payment_method):
    """Generate a unique 12-character alphanumeric reference based on payment method."""
    unique_id = str(uuid.uuid4().int)[:9]
    # unique_id = uuid.uuid4().hex[:9].upper()

    if payment_method == "M-Pesa":
        return f"MPS{unique_id}"
    elif payment_method == "Cash":
        return f"CSH{unique_id}"
    else:
        return f"OTH{unique_id}"

def generateSubscriptionID(reference, member_id):
    """
    - Get reference first 7 characters from reference and concatenate
    - to memberid as a post_fix
    """
    timestamp = str(int(time.time()))[-5:]
    return f"{reference[:7]}{member_id}{timestamp}"
