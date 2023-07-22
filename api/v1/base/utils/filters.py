import django_filters
from django_filters import FilterSet

from senat.models import Sponsor


class CreatedRangeFilter(FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Sponsor
        fields = []
