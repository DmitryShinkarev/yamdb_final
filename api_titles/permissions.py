from rest_framework.permissions import BasePermission, SAFE_METHODS

from api_users.models import UserRoles


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return bool(
                (request.user and request.user.is_staff)
                or request.user.role == UserRoles.ADMIN
            )

        return False


class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(
                (request.user and request.user.is_staff)
                or request.user.role == UserRoles.ADMIN
                or request.user.role == UserRoles.MODERATOR
            )

        return False


class IsModeratorOrAdminOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True

        if request.user.is_authenticated:
            return bool(
                (request.user and request.user.is_staff)
                or request.user.role == UserRoles.ADMIN
                or request.user.role == UserRoles.MODERATOR
            )

        return False


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)
