from tokenize import Token  
from django.core.serializers import serialize  # Импортируем функцию serialize для преобразования модели в json
from django.forms import model_to_dict  # Импортируем функцию model_to_dict 
from django.shortcuts import render  # Импортируем функцию render 
from rest_framework.response import Response  # Импортируем функцию Response для
from rest_framework.viewsets import ModelViewSet  # Импортируем класс ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView  # Импортируем функции для работы с сериализаторами  
from rest_framework.decorators import action  # Импортируем декоратор action для работы с дополнительными маршрутами
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # Импортируем дополнительные права для работы с дополнительными маршрутами
from rest_framework.authentication import TokenAuthentication  # Импортируем класс для работы с токенами
from rest_framework.pagination import PageNumberPagination  # Импортируем класс для работы с пагинацией
from .models import Men, Category  # Импортируем модели из файла models
from .serializers import MenSerializer  # Импортируем сериализатор из файла serializers
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly  # Импортируем самописные права из файла permissions


class MenAPIListPagination(PageNumberPagination):  # Класс отвечающий за обработку get (возвращает записи)
    page_size = 4  # Устанавливаем количество элементов на одной странице
    page_size_query_param = 'page_size'  # Для пользовательской устанавки количества элементов на одной странице
    max_page_size = 100  # Устанавливаем максимальное количество элементов на странице

class MenAPIList(ListCreateAPIView):  # Класс отвечающий за обработку get (возвращает записи)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать  
    permission_classes= (IsAuthenticatedOrReadOnly, )  # Добавляем права IsAuthenticatedOrReadOnly  
    pagination_class = MenAPIListPagination  # Добавляем класс пагинации

class MenAPIUpdate(RetrieveUpdateAPIView):  # Класс отвечающий за обработку put и patch (изменение записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    permission_classes = (IsAuthenticated, )  # Добавляем права IsAuthenticated
    # authentication_classes = (TokenAuthentication, )  # Добавляем дополнительно права TokenAuthentication комментим, чтобы иметь возможность работать именно с JWT токенами

class MenAPIDestroy(RetrieveDestroyAPIView):  # Класс отвечающий за delete запросы
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    permission_classes = (IsOwnerOrReadOnly, )  # Добавляем самописные права IsOwnerOrReadOnly


































# class MenViewSet(ModelViewSet):  # Класс отвечающий за обработку get, post, patch и delete на основе базового класса ModelViewSet
#     # queryset = Men.objects.all()  # Получаем список всех записей из БД. Если убираем отсюда, то запросы не будут работать, если не прописать basename='men' в роутере.
#     serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')  # Получаем pk из url

#         if not pk:  # Если pk не передан
#             return Men.objects.all()[:3]  # Возвращаем список из трех первых записей из БД    
            
#         return Men.objects.filter(pk=pk)  # Возвращаем запись отфильрованную по id
        
#     @action(methods=['get'], detail=False)  # Добавляем декоратор для обработки get запросов. Detail=False - выводит все записи, Detail=True - выводит одну запись
#     def category(self, request):  # Метод отвечающий за вывод всех категорий записей
#         cats = Category.objects.all()  # Получаем список всех категорий
#         return Response({'cats': [cat.name for cat in cats]})  # Возвращаем имена категорий. Они доступны по адресу http://127.0.0.1:8000/api/v1/men/category/   