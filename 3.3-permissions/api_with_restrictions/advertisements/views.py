from django.db.migrations import serializer
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrIsAdminOrReadOnly, IsNotOwner, IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    status = filters.DjangoFilterBackend
    creator = filters.DjangoFilterBackend

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    # permission_classes = [IsAdminUser, ]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated(), ]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsAdminOrReadOnly(), ]
        if self.action in ["retrieve"] and Advertisement.objects.get(id=self.kwargs['pk']).status == "DRAFT":
            print(self)
            return [IsAuthenticated(), IsOwnerOrReadOnly(), ]
        return []


class FavoriteViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filterset_fields = ['user', 'advertisement']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "destroy":
            return [IsAuthenticated(), IsOwnerOrIsAdminOrReadOnly(), ]
        if self.action in ["create", "update", "partial_update", ]:
            return [IsAuthenticated(), IsNotOwner(), ]
        return []
