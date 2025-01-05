from django.contrib import admin
from django.urls import path

from menapp.views import MenAPIList, MenAPIUpdate, MenAPIDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenAPIList.as_view()),
    path('api/v1/menlist/<int:pk>/', MenAPIUpdate.as_view()),
    path('api/v1/mendetail/<int:pk>/', MenAPIDetailView.as_view()),
]
