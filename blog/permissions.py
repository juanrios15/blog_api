from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return obj.user == request.user


class IsOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class IsSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("entra a revisar esto")
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        else:
            return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
