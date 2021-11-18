from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from blog.models import Article
from comments.models import Comment

User = get_user_model()


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser


class OwnerAndAdmin(IsAuthenticated):
    """This permissions is only True for
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


class OwnerOrAdminOrAuthorOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        if isinstance(obj, (Article, Comment)) and obj.author == request.user:
            return True

        if isinstance(obj, Comment) and obj.content_object.author == request.user:
            return True

        if request.method in SAFE_METHODS:
            return True

        return False


class FullProfile(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return all(
            user.birth_date,
            user.fname,
            user.lname,
            user.city,
            user.province,
            user.avatar_img,
        )


class FullProfileOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return all(
            user.birth_date,
            user.fname,
            user.lname,
            user.city,
            user.province,
            user.avatar_img,
        ) or request.method in SAFE_METHODS
