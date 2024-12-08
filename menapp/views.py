from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework import generics
from .models import Men
from .serializers import MenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



class MenAPIView(APIView):
    def get(self, request):  # Метод отвечающий за обработку get запросов
        lst = Men.objects.all().values()  # Получаем список всех записей из БД Men c помощью values
        return Response({'posts': list(lst)})  # Возвращаем список всех записей с ключем posts

    def post(self, request):  # Метод отвечающий за обработку post запросов
        post_new = Men.objects.create(
            title = request.data['title'],
            content = request.data['content'],
            cat_id = request.data['cat_id'],
        )
        return Response({'post': model_to_dict(post_new)})  # Вернем наши добавленные данные, преобразовав из в словарь


# class MenAPIView(generics.ListAPIView):
#     queryset = Men.objects.all()
#     serializer_class = MenSerializer