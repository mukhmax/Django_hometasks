from rest_framework.permissions import BasePermission


class IsOwnerOrIsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.is_staff


class IsNotOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user != obj.user


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
