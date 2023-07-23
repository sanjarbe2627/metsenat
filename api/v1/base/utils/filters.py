import django_filters
from django_filters import FilterSet


class CreatedRangeFilter(FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at__date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at__date', lookup_expr='lte')
