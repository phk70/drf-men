from django.contrib import admin
from django.urls import path

from menapp.views import MenViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenViewSet.as_view({'get': 'list'})),
    path('api/v1/menlist/<int:pk>/', MenViewSet.as_view({'put': 'update'})),
]
