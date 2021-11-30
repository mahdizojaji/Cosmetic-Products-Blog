from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

from blog.models import Article
from comments.models import Comment

User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class OwnerAndAdmin(BasePermission):
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


class OwnerAndAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        if isinstance(obj, (Article, Comment)) and obj.author == request.user:
            return True

        return False


class OwnerOrAdminOrAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        if isinstance(obj, (Article, Comment)) and obj.author == request.user:
            return True

        if isinstance(obj, Comment) and obj.content_object.author == request.user:
            return True

        return False


class FullProfile(BasePermission):
    message = 'You must have a full profile to access this resource'

    def has_permission(self, request, view):

        user = request.user
        return user.is_authenticated and all([
            user.birth_date, user.fname, user.lname, user.city, user.province, user.avatar_img,
        ])


class FullProfileOrReadOnly(BasePermission):
    message = 'You must have a full profile to access this resource'

    def has_permission(self, request, view):
        user = request.user
        return request.method in SAFE_METHODS or (user.is_authenticated and all([
            user.birth_date, user.fname, user.lname, user.city, user.province, user.avatar_img
        ]))
