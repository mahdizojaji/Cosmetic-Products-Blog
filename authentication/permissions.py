from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model

from blog.models import Article
from comments.models import Comment

User = get_user_model()


class OwnerAndAdmin(IsAuthenticated):
    """This premissions is only True for
    Authenticated Admin or Owner itself"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        if isinstance(obj, (Article, Comment)) and obj.author == request.user:
            return True

        return False


class OwnerAndAdminOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        if isinstance(obj, (Article, Comment)) and obj.author == request.user:
            return True

        if request.method in SAFE_METHODS:
            return True

        return False
