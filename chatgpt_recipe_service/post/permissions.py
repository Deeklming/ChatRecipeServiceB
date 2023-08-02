from rest_framework import permissions


class NewReadOnly(permissions.BasePermission):

    def has_permission(self, req, view):
        if req.method == 'GET':
            return True
        return req.user.is_authenticated

    def has_object_permission(self, req, view, obj):
        if req.method in permissions.SAFE_METHODS:
            return True
        return obj.user == req.user
