from rest_framework import permissions


class Isvendor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "VENDOR":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "VENDOR":
            return True
        return False