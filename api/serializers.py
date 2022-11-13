from rest_framework.serializers import (IntegerField, CharField, Serializer,
ModelSerializer, HyperlinkedIdentityField, SerializerMethodField)
from notes.models import Note
from django.contrib.auth import get_user_model


class NoteSerializer(ModelSerializer):
    # author = SerializerMethodField(read_only=True)

    # def get_author(self, obj):
    #     return str(obj.author.email)

    class Meta:
        model = Note
        fields = '__all__'


class ThinNoteSerializer(ModelSerializer):
    # author = SerializerMethodField(read_only=True)

    # def get_author(self, obj):
    #     return str(obj.author.email)

    class Meta:
        model = Note
        fields = ('id', 'title')


# class NoteSerializer(Serializer):
#     id = IntegerField(read_only=True)
#     title = CharField(required=True, max_length=250)
#     text = CharField(required=False, allow_blank=True)
#
#     def create(self, validated_data):
#         '''
#         validated_data данные, которые прошли проверку на наличии этих полей
#         и на соответствие указанным параметрам.
#         Если происходит валидация, то записываем данные
#         '''
#         return Note.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance

