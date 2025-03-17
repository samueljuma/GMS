from rest_framework import permissions

class IsAdminOrTrainer(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins to manage both Trainers and Members.
    - Trainers can only manage Members (can add, view, and approve but not modify them).
    - Members cannot perform any actions.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and has permission based on their role."""
        if not request.user.is_authenticated:
            return False

        # Read access (GET, HEAD, OPTIONS) is allowed for Admins and Trainers
        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["Admin", "Trainer"]

        # Allow user creation (Admins create Trainers & Members, Trainers create Members)
        if request.method == "POST":
            return request.user.role in ["Admin", "Trainer"]

        # Only Admins can update or delete users, EXCEPT for the custom "approve" action
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Check if it's an "approve" action, which Trainers can do for Members
            if view.action == "approve":
                return request.user.role in ["Admin", "Trainer"]
            return request.user.role == "Admin"  # Other updates only allowed for Admins

        return False  # Deny access otherwise

    def has_object_permission(self, request, view, obj):
        """Admins can modify anyone, Trainers can only manage Members (view, add, approve)."""
        if request.user.role == "Admin":
            return True  # Admins can manage Trainers and Members

        if request.user.role == "Trainer" and obj.role == "Member":
            # Trainers can read (GET) and create (POST) Members
            if request.method in ["GET", "POST"]:
                return True
            
            # Trainers can also approve Members (custom action)
            if view.action == "approve":
                return True

        return False  # Deny access otherwise

