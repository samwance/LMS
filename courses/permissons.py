from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().owner


class IsOwnerOrStaffView(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user == obj.is_staff:
            return True
        return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):

        return request.user == view.get_object().owner


class IsNotStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return False


class IsNotStaffView(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.is_staff:
            return False
