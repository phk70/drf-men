from rest_framework import serializers
from .models import Men
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io


class MenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Men
        fields = ('title', 'content', 'cat')
        # fields = __all__      Если хотим просто выводить все поля

