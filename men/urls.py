from django.contrib import admin
from django.urls import path

from menapp.views import MenAPIView, MenAPIList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenAPIList.as_view()),
    path('api/v1/menlist/<int:pk>/', MenAPIList.as_view()),
]
