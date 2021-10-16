from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class IsCreator(permissions.BasePermission):

   
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.method in permissions.SAFE_METHODS:
        #    return True
                
        # Write permissions are only allowed to the owner of the snippet.
        if obj.owner == request.user:
            return True
        else:
            return False
            

SAFE_METHODS_SNIPPETLIST = [
    'POST','HEAD', 'OPTIONS'
]

class SnippetListPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS_SNIPPETLIST:
            return True

        return False


class IsAdminOrCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user or request.user.is_staff:
            return True
        return False
    