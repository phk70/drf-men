from django.core.serializers import serialize
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
        serializer.save()  # Сохраняем данные. Автоматически вызовется метод Create из сериализатора
        return Response({'post': serializer.data})  # Вернем наши добавленные данные
    
    def put(self, request, *args, **kwargs):  # Метод отвечающий за обработку put запросов
        pk = kwargs.get('pk', None)  # Получаем id записи
        if not pk:  # Если id не передан
            return Response({'Ошибка': 'Метод PUT не может быть выполнен'})  # Возвращаем ошибку
        try:
            instance = Men.objects.get(pk=pk)  # Получаем запись по id
        except:
            return Response({'Ошибка': 'Объект не существует'})  # Если запись не найдена возвращаем ошибку
        
        serializer = MenSerializer(data=request.data, instance=instance)  # Помещаем принятые данные в объект сериализатора
        serializer.is_valid(raise_exception=True)  # Проверяем корректность принятых данных согласно тому что прописано в serializers.py
        serializer.save()  # Сохраняем данные. Автоматически вызовется метод Update из сериализатора
        return Response({'post': serializer.data})  # Вернем наши добавленные данные


# class MenAPIView(generics.ListAPIView):
#     queryset = Men.objects.all()
#     serializer_class = MenSerializer