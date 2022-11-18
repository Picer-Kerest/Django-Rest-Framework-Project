from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        """
        Чтение или добавление
        Либо список, либо детализация,
        либо добавление записи
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        obj - объект - экземляр модели.

        Редактирование или удаление

        Если метод GET, то мы разрешаем просмотр

        Если авторизованный пользователь автор, тогда появляется
        возможность редактировать запись

        Если пользователь является администратором, то он имеет право на любое действие

        request.user обычно возвращает экземпляр django.contrib.auth.models.User
        """
        if request.method in SAFE_METHODS:
            return True
        if request.user.admin:
            return True
        else:
            return obj.author == request.user

