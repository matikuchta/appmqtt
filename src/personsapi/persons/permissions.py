from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.userrole.role in ['admin', 'manager']
        except AttributeError:
            return False

class IsManagerOrAdminForWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Use correct related name here
        user_role = getattr(request.user, 'role', None)
        return user_role and user_role.role in ['admin', 'manager']