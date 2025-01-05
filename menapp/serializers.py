from rest_framework import serializers
from .models import Men
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


# class MenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

class MenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)  # read_only=True значит поле только для чтения и не обязательно к заполнению, т.к. генерируется само
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()

    def create(self, validated_data):
        return Men.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.time_update = validated_data.get('time_update', instance.time_update)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.cat_id = validated_data.get('cat_id', instance.cat_id)
        instance.save()
        return instance


# # Для примера работы сериалайзера
# def encode():
#     model = MenModel('Григорий Лепс', 'Что то про Гришу Лепса')  # Создаем объект класса MenModel
#     model_sr = MenSerializer(model)  # Сериализуем его
#     print(model_sr.data, sep='\n')  # Выводим в консоль то что у нас получилось. Атрибут data - это сериализованные данные
#     json = JSONRenderer().render(model_sr.data)  # Преобразуем объект сериализации в байтовую json строку
#     print(json)  # Выводим в консоль то что у нас получилось.

#     # Проверяем работу через shell:
#     # python manage.py shell
#     # from menapp.serializers import encode
#     # encode()

# # Пример обратного преобразования
# def decode():
#     stream = io.BytesIO(b'{"title": "Grigory Leps", "content": "What is Grisha"}')  # Иммитируем вход байтовой строки 
#     data = JSONParser().parse(stream)  # Парсим
#     serializer = MenSerializer(data=data)  # объект сериализатора
#     serializer.is_valid()  # проверяем корректность данных
#     print(serializer.validated_data)  # если данные валидны - выводим колекцию этих данных

#     # Проверяем работу через shell:
#     # python manage.py shell
#     # from menapp.serializers import decode
#     # decode()