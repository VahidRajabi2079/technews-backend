from rest_framework.permissions import BasePermission

class IsNotAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated or request.user.is_staff
