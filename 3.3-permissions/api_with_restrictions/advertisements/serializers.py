from django.contrib.auth.models import User
from rest_framework import serializers, request
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at',)
        read_only_fields = ('creator',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию
        method = self.context['request'].method
        status = self.initial_data.get('status')
        opened = Advertisement.objects.filter(status='OPEN')
        user_opened = opened.filter(creator=self.context["request"].user)
        if method == "POST" and len(user_opened) >= 10 and not status or status == 'OPEN':
            raise ValidationError('Вы превысили максимальное количество активных объявлений.')
        if method in ["PUT", "PATCH"] and len(user_opened) >= 10 and status == 'OPEN':
            raise ValidationError('Вы превысили максимальное количество активных объявлений.')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""

    class Meta:
        model = Favorite
        fields = ('advertisement', 'user',)
        read_only_fields = ('user',)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        method = self.context['request'].method
        username = self.context['request'].user
        user = User.objects.get(username=username).id
        advertisement_id = self.initial_data.get('advertisement')
        creator_name = Advertisement.objects.get(id=advertisement_id).creator
        creator = User.objects.get(username=creator_name).id
        if method in ["POST", "PUT", "PATCH"] and user == creator:
            raise ValidationError('Создатель объявления не может добавлять его в избранное.')
        user = Favorite.objects.get(advertisement=advertisement_id, user=user)
        if method in ["POST", "PUT", "PATCH"] and user:
            raise ValidationError('Объявление уже добавлено пользователем в избранные.')
        return data
