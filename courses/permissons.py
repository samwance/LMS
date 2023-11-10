from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsOwner(BasePermission):
    message = "Необходимо иметь права владельца."

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return request.user == obj.owner
        return False


class IsModerator(BasePermission):
    message = "Необходимо иметь права модератора."

    def has_permission(self, request, view):
        if request.user.role == UserRole.MODERATOR:
            return True
        return False
