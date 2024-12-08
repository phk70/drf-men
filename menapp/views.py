from django.shortcuts import render

from rest_framework import generics
from .models import Men
from .serializers import MenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class MenAPIView(APIView):
    def get(self, request):  # Метод отвечающий за обработку get запросов
        return Response({'title': 'Майкл Джексон'})  # Response вернет просто фиксированные данные в виде JSON строки

    def post(self, request):  # Метод отвечающий за обработку post запросов
        return Response({'title': 'Майк Тайсон'})  # Вернем предопределенный JSON при отправке post запроса


# class MenAPIView(generics.ListAPIView):
#     queryset = Men.objects.all()
#     serializer_class = MenSerializer