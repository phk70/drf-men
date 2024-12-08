from rest_framework import serializers
from .models import Men
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io



class MenModel:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class MenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()


# Для примера работы сериалайзера
def encode():
    model = MenModel('Григорий Лепс', 'Что то про Гришу Лепса')  # Создаем объект класса MenModel
    model_sr = MenSerializer(model)  # Сериализуем его
    print(model_sr.data, sep='\n')  # Выводим в консоль то что у нас получилось. Атрибут data - это сериализованные данные
    json = JSONRenderer().render(model_sr.data)  # Преобразуем объект сериализации в байтовую json строку
    print(json)  # Выводим в консоль то что у нас получилось.

    # Проверяем работу через shell:
    # python manage.py shell
    # from menapp.serializers import encode
    # encode()

# Пример обратного преобразования
def decode():
    stream = io.BytesIO(b'{"title": "Grigory Leps", "content": "What is Grisha"}')  # Иммитируем вход байтовой строки 
    data = JSONParser().parse(stream)  # Парсим
    serializer = MenSerializer(data=data)  # объект сериализатора
    serializer.is_valid()  # проверяем корректность данных
    print(serializer.validated_data)  # если данные валидны - выводим колекцию этих данных

    # Проверяем работу через shell:
    # python manage.py shell
    # from menapp.serializers import decode
    # decode()