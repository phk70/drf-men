from django.core.serializers import serialize
from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Men
from .serializers import MenSerializer


class MenViewSet(ModelViewSet):  # Класс отвечающий за обработку get, post, patch и delete на основе базового класса ModelViewSet
    queryset = Men.objects.all()  # Получаем список всех записей из БД
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать