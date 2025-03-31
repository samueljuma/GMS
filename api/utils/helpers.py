import uuid

def generate_reference():
    """Generate a unique 12-character alphanumeric reference"""
    return uuid.uuid4().hex[:12].upper()  # Take the first 12 characters of a UUID
