from rest_framework import permissions


class Isadmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "ADMIN":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True
        return False