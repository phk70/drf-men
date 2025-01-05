from django.core.serializers import serialize
from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Men, Category
from .serializers import MenSerializer
from rest_framework.decorators import action


class MenViewSet(ModelViewSet):  # Класс отвечающий за обработку get, post, patch и delete на основе базового класса ModelViewSet
    # queryset = Men.objects.all()  # Получаем список всех записей из БД. Если убираем отсюда, то запросы не будут работать, если не прописать basename='men' в роутере.
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать

    def get_queryset(self):
        pk = self.kwargs.get('pk')  # Получаем pk из url

        if not pk:  # Если pk не передан
            return Men.objects.all()[:3]  # Возвращаем список из трех первых записей из БД    
            
        return Men.objects.filter(pk=pk)  # Возвращаем запись отфильрованную по id
        
    @action(methods=['get'], detail=False)  # Добавляем декоратор для обработки get запросов. Detail=False - выводит все записи, Detail=True - выводит одну запись
    def category(self, request):  # Метод отвечающий за вывод всех категорий записей
        cats = Category.objects.all()  # Получаем список всех категорий
        return Response({'cats': [cat.name for cat in cats]})  # Возвращаем имена категорий. Они доступны по адресу http://127.0.0.1:8000/api/v1/men/category/   