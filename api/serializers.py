from rest_framework.serializers import (IntegerField, CharField, Serializer,
ModelSerializer, HyperlinkedIdentityField, SerializerMethodField)
from notes.models import Note
from django.contrib.auth import get_user_model
# https://stackoverflow.com/questions/24629705/django-using-get-user-model-vs-settings-auth-user-model


class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        # queryset = model.objects.all()
        fields = ('id', 'email', 'password', 'name', 'admin')
        extra_kwargs = {'password': {'write_only': True}}
        # extra_kwargs Для того чтобы пароль нельзя было поменять с помощью запроса.

    def create(self, validated_data):
        # password = validated_data.pop('password', '')  # Второй способ сохранения пароля с хэшированием
        user = self.Meta.model(**validated_data)
        # user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


class NoteSerializer(ModelSerializer):
    author = SerializerMethodField(read_only=True)

    def get_author(self, obj):
        """
        Управление возвратом
        get_имя того поля, которое нам нужно найти
        Возвращать должно обязательно string

        После этого author будет возвращён не в виде id, а в виде email
        """
        return str(obj.author.email)

    class Meta:
        model = Note
        fields = '__all__'


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:notes-detail')
    # author = SerializerMethodField(read_only=True)
    #
    # def get_author(self, obj):
    #     return str(obj.author.email)

    class Meta:
        model = Note
        fields = ('id', 'title', 'url')


# class NoteSerializer(Serializer):
#     id = IntegerField(read_only=True)
#     title = CharField(required=True, max_length=250)
#     text = CharField(required=False, allow_blank=True)
#
#     def create(self, validated_data):
#         """
#         validated_data данные, которые прошли проверку на наличии этих полей
#         и на соответствие указанным параметрам.
#         Если происходит валидация, то записываем данные
#         """
#         return Note.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance

