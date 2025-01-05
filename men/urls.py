from django.contrib import admin
from django.urls import include, path

from menapp.views import MenViewSet
from rest_framework import routers


router = routers.DefaultRouter()  # Создаем объект роутера для работы с маршрутами
router.register(r'men', MenViewSet, basename='men')  # Регистрируем в нем наш класс вьюсета MenViewSet. basename='men' - название маршрута. Он обязателен если мы удаляем стандартную переменную queryset из нашего вьюсета

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # маршрут для нашего MenViewSet с использованием роутера. Теперь адрес http://127.0.0.1:8000/api/v1/men/       
]
