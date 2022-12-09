from django.contrib.auth.models import User
from rest_framework import serializers, request
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


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
