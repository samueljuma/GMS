from rest_framework import permissions
class IsAdminOrTrainer(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins to manage both Trainers and Members.
    - Trainers can only manage Members.
    - Members cannot perform any actions.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and has permission based on their role."""
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:  # Allow read-only access to Admins and Trainers
            return request.user.role in ["Admin", "Trainer"]

        # Admins can create/update/delete users, Trainers can only create Members
        if request.method == "POST":
            return request.user.role in ["Admin", "Trainer"] 

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user.role == "Admin"  # Only Admins can modify/delete users
        
        return False  # Deny access otherwise

    def has_object_permission(self, request, view, obj):
        """Admins can modify anyone, Trainers can only modify Members."""
        if request.user.role == "Admin":
            return True  # Admins can modify Trainers and Members
        
        if request.user.role == "Trainer" and obj.role == "Member":
            return request.method in ["GET", "POST"]  # Trainers can ADD and READ Members, but not modify
        
        return False  # Deny access otherwise
