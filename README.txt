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
Дописали методы создания и изменения в сериализаторе

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

Дописали метод для изменения записи в views
    
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

Создали новый маршрут в urls
    path('api/v1/menlist/<int:pk>/', MenAPIView.as_view()),

**********************************************************************************************************

Дописали в Views метод удаления поста

    def delete(self, request, *args, **kwargs):  # Метод отвечающий за обработку delete запросов
        pk = kwargs.get('pk', None)  # Получаем id записи
        if not pk:  # Если id не передан
            return Response({'Ошибка': 'Метод DELETE не может быть выполнен'})  # Возвращаем ошибку
        try:
            instance = Men.objects.get(pk=pk)  # Получаем запись по id
        except:
            return Response({'Ошибка': f'Объект {str(pk)} не существует'})  # Если запись не найдена возвращаем ошибку
        instance.delete()  # Удаляем запись
        return Response({'post': f'Удален объект {str(pk)}'})


VIEWS отвечает только за обработку запросов. А СЕРИАЛИЗАТОР отвечает за обработку данных

**********************************************************************************************************

6. Переписали сериалайзер с использованием наследования от ModelSerializer и вложенным классом Meta

class MenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Men
        fields = ('id', 'title', 'content', 'time_create', 'time_update', 'is_published', 'cat')


Так же существуют и базовые классы для представлений
CreateAPIView - создание данных по ПОСТ запросу
ListAPIView - чтение списка данных по ГЕТ запросу
RetrieveAPIView - чтение конкретных данныхпо ГЕТ запросу
DestroyAPIView - удаление по ДЕЛИТ запросу
UpdateAPIView - изменение записей по ПУТ или ПАТЧ запросу
ListCreateAPIView - чтение по ГЕТ и создание списка по ПОСТ
RetrieveUpdeteAPIView - чтение и изменение отдельной записи по ГЕТ
RetrieveDestroyAPIView - чтение по ГЕТ и удаление по ДЕЛИТ 
RetrieveUpdeteDestroyAPIView - чтоние, изменение и добавление данных по ГЕТ, ПУТ, ПАТЧ и ДЕЛИТ


Перепишем методы GET и POST из нашего текущего класса в новый класс MenAPIList

from rest_framework.generics import ListCreateAPIView 


class MenAPIList(ListCreateAPIView):  # Класс отвечающий за обработку get (возвращает записи) и post запросов (добавлениие записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать  

Идобавим его в маршруты

from menapp.views import MenAPIView, MenAPIList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenAPIList.as_view()),
    path('api/v1/menlist/<int:pk>/', MenAPIList.as_view()),
]

теперь на сайте все так же будут отображаться все записи, а так же внизу появится возможность через форму добавлять записи 

**********************************************************************************************************

7. Удалим ранее созданный класс в View с его методами и создадим новый класс отвечающий за изменение записей на основе базового класса

from rest_framework.generics import ListCreateAPIView, UpdateAPIView


class MenAPIUpdate(UpdateAPIView):  # Класс отвечающий за обработку put и patch (изменение записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать

Изменим маршрут 

from menapp.views import MenAPIList, MenAPIUpdate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenAPIList.as_view()),
    path('api/v1/menlist/<int:pk>/', MenAPIUpdate.as_view()),
]


Так же добавим еще класс для просмотра/изменения и удаления данных.


from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView


class MenAPIDetailView(RetrieveUpdateDestroyAPIView):  # Класс отвечающий за обработку get, post, patch и delete запросов
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer

И новый маршрут для нашего


from menapp.views import MenAPIList, MenAPIUpdate, MenAPIDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenAPIList.as_view()),
    path('api/v1/menlist/<int:pk>/', MenAPIUpdate.as_view()),
    path('api/v1/mendetail/<int:pk>/', MenAPIDetailView.as_view()),
]

Теперь с использованием этого класса мы можем смотреть конкретную запись, изменять ее и удалить




Добавили коллекцию REST_FRAMEWORK в файл settings для отключения режима при релизе продукта (пока только прописал, но закоментировал)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Определяет что работаем с JSON
        'rest_framework.renderers.BrowsableAPIRenderer',  # Подключаем работу с данными через браузер
    ]
}

Именно строчку 'rest_framework.renderers.BrowsableAPIRenderer' нужно закоментировать перед релизом, чтобы пользователь не мог удалять и изменять данные через браузер


**********************************************************************************************************

8. Сейчас у нас во всех классах дуюлируются строки 
queryset = Men.objects.all()
serializer_class = MenSerializer

Чтобы это исправить используем ViewSets

Их существует не много:
ViewSet
GenericSet
ModelViewSet
ReadOnlyModelViewSet

Используем ModelViewSet т.к. наше представление работает с моделями


from rest_framework.viewsets import ModelViewSet


class MenViewSet(ModelViewSet):  # Класс отвечающий за обработку get, post, patch и delete на основе базового класса ModelViewSet
    queryset = Men.objects.all()  # Получаем список всех записей из БД
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать


В путях так же меняем 

from menapp.views import MenViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menlist/', MenViewSet.as_view({'get': 'list'})),
    path('api/v1/menlist/<int:pk>/', MenViewSet.as_view('put': 'update')),
]

Здесь в MenViewSet.as_view({'get': 'list'})
'get' - какой метод будем использовать для обработки запроса
'list' - метод который будет вызываться в самом вьюсете для обработки этого get запроса (весь список этих методов доступен в документации)