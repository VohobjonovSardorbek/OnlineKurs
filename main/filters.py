
from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    instructor = filters.CharFilter(field_name="instructor__username", lookup_expr="icontains")

    class Meta:
        model = Course
        fields = ['min_price', 'max_price', 'instructor']
