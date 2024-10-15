from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsOwnerOrReadOnlyPostFree(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method == "POST" or request.method == "GET":
            return True

        return obj.user == request.user


class IsOwnerChildPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj, multiple=False):

        return obj.child.parent.user == request.user


class IsAuthenticatedOrPostOnly(IsAuthenticated):
    """
    Custom permission to allow only authenticated users to access GET, PUT, and PATCH methods.
    Allows anyone to access the POST method.
    """

    def has_permission(self, request, view):
        if request.method == "POST" or request.method == "GET":
            return True

        return super().has_permission(request, view)


class IsOwnerParent(IsAuthenticated):
    def has_object_permission(self, request, view, obj, multiple=False):

        return obj.user == request.user
