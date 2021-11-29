from django_filters import rest_framework as filters

from .models import Course, Article


class CourseFilter(filters.FilterSet):
    author = filters.UUIDFilter(field_name="author__uuid")
    status = filters.CharFilter(method="filter_status")
    ordering = filters.OrderingFilter(fields=("slug", "cost", "id"))
    max_cost = filters.NumberFilter(field_name="cost", lookup_expr="lte")
    min_cost = filters.NumberFilter(field_name="cost", lookup_expr="gte")

    @staticmethod
    def filter_status(queryset, name, value):
        status_map = {
            # "0": Course.DRAFT,
            "1": Course.PENDING,
            "2": Course.PUBLISHED,
            # "draft": Course.DRAFT,
            "pending": Course.PENDING,
            "published": Course.PUBLISHED,
        }
        return queryset.filter(status=status_map.get(f"{value}".lower(), None))

    class Meta:
        model = Course
        fields = ("author", "slug", "status", "is_online", "cost", "max_cost", "min_cost")


class ArticleFilter(filters.FilterSet):
    author = filters.UUIDFilter(field_name="author__uuid")
    status = filters.CharFilter(method="filter_status")
    ordering = filters.OrderingFilter(fields=("slug", "id"))

    @staticmethod
    def filter_status(queryset, name, value):
        status_map = {
            "0": Article.DRAFT,
            "1": Article.PENDING,
            "2": Article.PUBLISHED,
            "draft": Article.DRAFT,
            "pending": Article.PENDING,
            "published": Article.PUBLISHED,
        }
        return queryset.filter(status=status_map.get(f"{value}".lower(), None))

    class Meta:
        model = Article
        fields = ("author", "slug", "status")
