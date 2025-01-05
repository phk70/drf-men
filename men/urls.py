from django.contrib import admin
from django.urls import include, path

from menapp.views import MenViewSet
from rest_framework import routers


router = routers.DefaultRouter()  # Создаем объект роутера для работы с маршрутами
router.register(r'men', MenViewSet)  # Регистрируем в нем наш класс вьюсета MenViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # маршрут для нашего MenViewSet с использованием роутера. Теперь адрес http://127.0.0.1:8000/api/v1/men/       
]
