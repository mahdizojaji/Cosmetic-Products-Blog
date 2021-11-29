from django_filters import rest_framework as filters

from .models import Course


class CourseFilter(filters.FilterSet):
    author = filters.UUIDFilter(field_name="author__uuid")
    status = filters.CharFilter(method="filter_status")
    ordering = filters.OrderingFilter(fields=("slug", "cost", "id"))

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
        fields = ("author", "slug", "status", "cost", "is_online")
