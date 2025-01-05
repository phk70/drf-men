from rest_framework import serializers
from .models import Men
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


class MenSerializer(serializers.ModelSerializer):  # Создаем класс  сериализатора который наследуем от базового класса
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Добавляем автоматическое заполнение скрытого поля user именем текущего юзера

    class Meta:
        model = Men  # Указываем модель
        fields = '__all__'  # Выводим все поля
        # fields = ('title', 'content', 'cat')  # Выведет поля title, content, cat
        

