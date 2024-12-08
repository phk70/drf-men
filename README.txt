Комментируем generics.ListAPIView и разбираем работу view на примере базового класа APIView
Пробуем методы get и post. Если метод явно не прописан в классе, то запрос ничего не вернет
Базовый класс APIView сам сгенерирует сообщение о том, что этот метод не разрешен.

Теперь по get запросу будем отправлять список всех данных из БД Men
А в post запросе сделали возможность добавления записей в БД
При отправке в postman post запроса во вкладке Body + Row
{
    "title": "Павел",
    "content": "Что то с чем то",
    "cat_id": 1
}
в БД добавится новая запись
Так же есть методы:
-get 
-post
-put
-patch
-delete

Базовый класс APIView как раз и связывает пришедший запрос с соответствующим методом.

**********************************************************************************************************
Прописываем сериализатор. Он конвертирует произвольные объекты языка python в формат json (или реже xml) и обратно.
В serialized.py определим класс MenModel объекты которого будем преобразовывать в json и обратно
Написали функции code и encode
Проверили их работу

**********************************************************************************************************
Переписываем сериализатор конкретно для нашей модели. Со всеми полями указанными в моделях
class MenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat = serializers.IntegerField()

После этого его можно использовать в views в MenAPIView

Переписали get и post методы
class MenAPIView(APIView):
    def get(self, request):  # Метод отвечающий за обработку get запросов
        m = Men.objects.all()  # Получаем список всех записей из БД Men как queryset
        return Response({'posts': MenSerializer(m, many=True).data})  # Передаем на вход сериализатора весь queryset. Параметр many т.к. у нас список а не одно значение 

    def post(self, request):  # Метод отвечающий за обработку post запросов
        serializer = MenSerializer(data=request.data)  # Помещаем принятые данные в объект сериализатора
        serializer.is_valid(raise_exception=True)  # Проверяем корректность принятых данных согласно тому что прописано в serializers.py. Rise_exception - генерирует ответ в формате json с исключениями в случае ошибки с расшифровкой этих ошибок вместо обычной страницы с ошибкой
        post_new = Men.objects.create(
            title = request.data['title'],
            content = request.data['content'],
            cat_id = request.data['cat_id']
        )
        return Response({'post': MenSerializer(post_new).data})  # Вернем наши добавленные данные

**********************************************************************************************************
