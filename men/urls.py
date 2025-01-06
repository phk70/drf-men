from django.contrib import admin  # импортируем админку для управления БД
from django.urls import include, path, re_path  # импортируем функцию path для создания маршрутов

from menapp.views import MenAPIList, MenAPIUpdate, MenAPIDestroy  # импортируем наши вьюсеты из нашего приложения
# from rest_framework import routers


# router = routers.DefaultRouter()  # Создаем объект роутера для работы с маршрутами
# router.register(r'men', MenViewSet, basename='men')  # Регистрируем в нем наш класс вьюсета MenViewSet. basename='men' - название маршрута. Он обязателен если мы удаляем стандартную переменную queryset из нашего вьюсета

urlpatterns = [  
    path('admin/', admin.site.urls),  # маршрут админки для управления БД
    path('api/v1/drf-auth/', include('rest_framework.urls')),  # маршрут для авторизации
    path('api/v1/men/', MenAPIList.as_view()),  #  Маршрут для отображения всех записей
    path('api/v1/men/<int:pk>/', MenAPIUpdate.as_view()),  # Маршрут для изменения записей по идентификатору
    path('api/v1/mendelete/<int:pk>/', MenAPIDestroy.as_view()),  # Маршрут для удаления записей по идентификатору
    path('api/v1/auth/', include('djoser.urls')),  # маршрут для работы с токенами
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # маршрут для работы с токенами
]
