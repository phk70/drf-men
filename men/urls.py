from django.contrib import admin
from django.urls import path

from menapp.views import MenAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenAPIView.as_view()),
    path('api/v1/menlist/<int:pk>/', MenAPIView.as_view()),
]
