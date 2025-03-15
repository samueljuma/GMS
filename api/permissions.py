from rest_framework import permissions

class IsAdminOrTrainer(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admins to manage both Trainers and Members
    - Trainers to manage only Members
    """
    def has_permission(self, request, view):
        """Check if the user is authenticated and has a valid role."""
        return request.user.is_authenticated and request.user.role in ["Admin", "Trainer"]

    def has_object_permission(self, request, view, obj):
        """Admins can modify anyone, Trainers can only modify Members."""
        if request.user.role == "Admin":
            return True  # Admins can modify Trainers and Members
        
        if request.user.role == "Trainer" and obj.role == "Member":
            return True  # Trainers can only modify Members
        
        return False  # Deny access otherwise
