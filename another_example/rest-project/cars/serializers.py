from rest_framework import serializers
from .models import Car


class CarDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # При каждом создании пользователь создаётся сам. Поле будет скрыто.
    # Также его нельзя менять.
    # Вставляет пользователя из request
    # Без авторизации будет ошибка

    class Meta:
        model = Car
        fields = '__all__'


class CarsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'vin', 'user')

