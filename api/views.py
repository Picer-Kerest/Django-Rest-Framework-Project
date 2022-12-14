from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from notes.models import Note
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin)
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import NoteSerializer, ThinNoteSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .permissions import IsAuthorOrReadOnly
# https://developer.mozilla.org/ru/docs/Web/HTTP/Status


class UserViewSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )
    # Новых пользователей может создавать только администратор


class NoteViewSet(ModelViewSet):
    model = Note
    queryset = model.objects.none()  # Пустой queryset
    serializer_class = NoteSerializer
    permission_classes = (IsAuthorOrReadOnly, )  # Установка прав
    # http_method_names = ['get', 'post'] # Доступные методы для этого ViewSet'a

    # def list(self, request, *args, **kwargs):
    #     notes = Note.objects.all()
    #     # notes = Note.objects.filter(author=request.user.id)
    #     context = {'request': request}
    #     serializer = ThinNoteSerializer(notes, many=True, context=context)
    #     return Response(serializer.data)

    def get_serializer_class(self):
        """
        Вместо метода list, который занимает много места, определяем этот метод
        В нашем методе list меняется только сериализатор

        self.action - действие, которое сейчас происходит. Только во ViewSet'ax
        """
        if self.action == 'list':
            return ThinNoteSerializer
        return NoteSerializer

    def get_queryset(self):
        """
        Переопределение queryset'a таким образом,
        чтобы пользователь видел только созданные им записи.
        Admin будет видеть все записи

        user имеет поле admin, которое прописано в accounts/models
        """
        if self.request.user.admin:
            return self.model.objects.all()
        return self.model.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        """
        request.user обычно возвращает экземпляр django.contrib.auth.models.User
        """
        serializer.save(author=self.request.user)


# class NoteListView(ListCreateAPIView):
#     """
#     Base of ListCreateAPIView:
#
#     class ListCreateAPIView(mixins.ListModelMixin,
#                         mixins.CreateModelMixin,
#                         GenericAPIView):
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#     """
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def list(self, request, *args, **kwargs):
#         """
#         Redefinition of queryset'a
#         """
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#
# class NoteDetailView(RetrieveUpdateDestroyAPIView):
#     """
#     PATCH при изменении одного или более полей одного объекта.
#     PUT когда изменяем всё или добавляем новый объект.
#
#     Используется для read-write-delete для представления одного экземпляра модели.
#     Предоставляет обработчики методов get, put, patch и delete.
#     Расширяет: GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
#     """
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer


# class NoteListView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def get(self, request, *args, **kwargs):
#         self.serializer_class = ThinNoteSerializer
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class NoteDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class NoteListView(APIView):
#     def get(self, request, format=None):
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class NoteDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Note.objects.get(pk=pk)
#         except Note.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk, format=None):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         note = self.get_object(pk)
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def notes_list(request, format=None):
#     if request.method == 'GET':
#         notes = Note.objects.all()
#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def notes_detail(request, pk, format=None):
#     try:
#         note = Note.objects.get(pk=pk)
#     except Note.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

