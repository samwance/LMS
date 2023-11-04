from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().owner


class IsOwner(BasePermission):
    def has_permission(self, request, view):

        return request.user == view.get_object().owner


class IsNotStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return False
