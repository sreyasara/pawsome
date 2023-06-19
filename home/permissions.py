# create permission.py file in home app
#
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.permissions import AllowAny


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


# is owner
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.is_authenticated and obj.user == request.user
