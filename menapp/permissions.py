from rest_framework import permissions  # Импортируем модуль предоставления прав permissions


class IsAdminOrReadOnly(permissions.BasePermission):  # Наследуем от базового класса BasePermission
    def has_permission(self, request, view):  # И переопределяем его базовый метод has_permission
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = GET, HEAD, OPTIONS
            return True  # True - разрешено. Даем доступ всем

        return bool(request.user and request.user.is_staff)  # Если не SAFE_METHODS, то только для админа
    

class IsOwnerOrReadOnly(permissions.BasePermission):  # Наследуем от базового класса BasePermission
    def has_object_permission(self, request, view, obj):  # И переопределяем его базовый метод has_object_permission
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = GET, HEAD, OPTIONS
            return True  # True - разрешено. Даем доступ всем

        return obj.user == request.user  # Если автор записи == текущему юзеру, то тоже возвращаем True и даем доступ