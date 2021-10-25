from rest_framework.permissions import IsAuthenticated


class OwnerAndAdmin(IsAuthenticated):
    """This premissions is only True for
    Authenticated Admin or Owner itself"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj == request.user:
            return True

        return False


class OwnerAndAdminOrReadOnly(IsAuthenticated):
    pass
