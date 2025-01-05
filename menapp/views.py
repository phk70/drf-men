from django.core.serializers import serialize
from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from .models import Men
from .serializers import MenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



class MenAPIList(ListCreateAPIView):  # Класс отвечающий за обработку get (возвращает записи) и post запросов (добавлениие записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать  

class MenAPIUpdate(UpdateAPIView):  # Класс отвечающий за обработку put и patch (изменение записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    
class MenAPIDetailView(RetrieveUpdateDestroyAPIView):  # Класс отвечающий за обработку get, post, patch и delete запросов
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer