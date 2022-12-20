from django_filters import rest_framework as filters
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    status = filters.DjangoFilterBackend
    creator = filters.DjangoFilterBackend
    """Фильтры для объявлений."""

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
