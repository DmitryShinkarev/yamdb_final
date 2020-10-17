from rest_framework.permissions import BasePermission

from api_users.models import UserRoles


class IsOwnProfileOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(
                (request.user and request.user.is_staff)
                or request.user.role == UserRoles.ADMIN
                or view.kwargs.get('username') == 'me'
            )

        return False
