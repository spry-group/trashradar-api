from rest_framework import permissions


class IsAdminOrAccountOwner(permissions.BasePermission):
    """
    Returns true if the request.user is owner of the account or Admin
    """
    def has_permission(self, request, view):
        """
        Returns true or false if the user has the permission
        :param view: View set
        :return: Boolean with the user permission
        """
        if request.user.is_authenticated():
            return True
        return False

    def has_object_permission(self, request, view, account):
        """
        Returns `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_authenticated():
            if request.user.is_staff:
                return True
            return account.username == request.user.username
        return False
