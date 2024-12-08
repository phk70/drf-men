from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework import generics
from .models import Men
from .serializers import MenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



class MenAPIView(APIView):
    def get(self, request):  # Метод отвечающий за обработку get запросов
        m = Men.objects.all()  # Получаем список всех записей из БД Men как queryset
        return Response({'posts': MenSerializer(m, many=True).data})  # Передаем на вход сериализатора весь queryset. Параметр many т.к. у нас список а не одно значение 

    def post(self, request):  # Метод отвечающий за обработку post запросов
        serializer = MenSerializer(data=request.data)  # Помещаем принятые данные в объект сериализатора
        serializer.is_valid(raise_exception=True)  # Проверяем корректность принятых данных согласно тому что прописано в serializers.py
        post_new = Men.objects.create(
            title = request.data['title'],
            content = request.data['content'],
            cat_id = request.data['cat_id']
        )
        return Response({'post': MenSerializer(post_new).data})  # Вернем наши добавленные данные


# class MenAPIView(generics.ListAPIView):
#     queryset = Men.objects.all()
#     serializer_class = MenSerializer