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
ModelViewSet - весь список операций CRUD
ReadOnlyModelViewSet - только чтение

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


Теперь добавим РОУТЕРЫ в urls.

from rest_framework import routers

router = routers.SimpleRouter()  # Создаем объект роутера для работы с маршрутами
router.register(r'men', MenViewSet)  # Регистрируем в нем наш класс вьюсета MenViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # маршрут для нашего MenViewSet с использованием роутера. Теперь адрес http://127.0.0.1:8000/api/v1/men/    
]

Благодаря одному вьюсету и роутеру у нас присутствуем весь функционал CRUD.



**********************************************************************************************************

9. Продолжение по Роутерам.
Есть 2 основных класса для роутеров:

SimpleRouter
DefauilRouter

Они практически идентичны. Только у DefaultRouter мы можем указать адрес http://127.0.0.1:8000/api/v1/ и он предложит перейти далее по men/  
А SimpleRouter принципиально ждет http://127.0.0.1:8000/api/v1/men/  и на все остальные выдает ошибку


Дополним функционал отдельным выводом списка категорий (по сути создадим новый маршрут .../men/category/)
Используем декоратор @action в нашем вьюсете

from rest_framework.response import Response
from rest_framework.decorators import action

class MenViewSet(ModelViewSet):  # Класс отвечающий за обработку get, post, patch и delete на основе базового класса ModelViewSet
    queryset = Men.objects.all()  # Получаем список всех записей из БД
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать

    @action(methods=['get'], detail=False)  # Добавляем декоратор для обработки get запросов. Detail=False - выводит все записи, Detail=True - выводит одну запись
    def category(self, request):  # Метод отвечающий за вывод всех категорий записей
        cats = Category.objects.all()  # Получаем список всех категорий
        return Response({'cats': [cat.name for cat in cats]})  # Возвращаем имена категорий. Они доступны по адресу http://127.0.0.1:8000/api/v1/men/category/ 



Для того, чтобы можно было нырять по категориям необходимо поменять флаг detail, дописать pk в выборке и вывод в return

    @action(methods=['get'], detail=True)  # Добавляем декоратор для обработки get запросов. Detail=False - выводит все записи, Detail=True - выводит одну запись
    def category(self, request, pk):  # Метод отвечающий за вывод всех категорий записей
        cats = Category.objects.get(pk=pk)  # Получаем список всех категорий
        return Response({'cats': cats.name})  # Возвращаем имя категории. 

Номер категории ставится перед ее именем
Теперь по GET запросу http://127.0.0.1:8000/api/v1/men/1/category/ обоюразится {'cats': 'Актеры'}
А по запросу http://127.0.0.1:8000/api/v1/men/2/category/ отобразится {'cats': 'Певцы'}



Сейчас наш вью сет доставет абсолютно все записи из базы благодаря queryset = Men.objects.all().
Чтобы поменять условия и например доставать только ТРИ записи необходимо его переопределить

def get_queryset(self):
        return Men.objects.all()[:3]  # Получаем список из трех первых записей из БД


Теперь стандартный   можно убрать, но тогда запросы не будут работать, если не прописать basename='men' в роутере.

router.register(r'men', MenViewSet, basename='men')  # Регистрируем в нем наш класс вьюсета MenViewSet. basename='men' - название маршрута. Он обязателен если мы удаляем стандартную переменную queryset из нашего вьюсета

имя men формируется автоматически от имени модели. Посмотреть его можно print(router.urls)

Но теперь не будет возможности просмотреть определенную запись по pk.
Исправляется следующим образом:

def get_queryset(self):
        pk = self.kwargs.get('pk')  # Получаем pk из url

        if not pk:  # Если pk не передан
            return Men.objects.all()[:3]  # Возвращаем список из трех первых записей из БД    
            
        return Men.objects.filter(pk=pk)  # Возвращаем запись отфильрованную по id




**********************************************************************************************************

10. Ограничения доступа (permissions)

В DRF 4 уровня
AllowAny - полный доступ
IsAuthenticated - только для авторизованных пользователей
IsAdminUser - только для Администраторов
IsAuthenticatedOrReadOnly - только авторизованным. Или всем, но только для чтения



Добавим в нашу модель дополнительное поле, которое будет хранить идентификатор пользователя

from django.contrib.auth.models import RetrieveUpdateDestroyAPIView

......
user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)


Проводим мграции и в базе данных появляется новое поле связанное с юзером




Возвращаем классы с методами вместо вьюсета для наглядности разграничения прав


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView 

class MenAPIList(ListCreateAPIView):  # Класс отвечающий за обработку get (возвращает записи) и post запросов
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать  


class MenAPIUpdate(RetrieveUpdateAPIView):  # Класс отвечающий за обработку put и patch (изменение записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать


class MenAPIDestroy(RetrieveDestroyAPIView):  # Класс отвечающий за delete запросы
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать




Маршруты так же возвращаем.


from menapp.views import MenAPIList, MenAPIUpdate, MenAPIDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/men/', MenAPIList.as_view()),  #  Маршрут для отображения всех записей
    path('api/v1/men/<int:pk>/', MenAPIUpdate.as_view()),  # Маршрут для изменения записей по идентификатору
    path('api/v1/mendelete/<int:pk>/', MenAPIDestroy.as_view()),  # Маршрут для удаления записей по идентификатору      
]



Права определяются в представлениях.

Установим права IsAuthenticatedOrReadOnly для class MenAPIList(ListCreateAPIView)


from rest_framework.permissions import IsAuthenticatedOrReadOnly

class MenAPIList(ListCreateAPIView):  # Класс отвечающий за обработку get (возвращает записи)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать  
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)  # Добавляем права IsAuthenticatedOrReadOnly  


И дописываем сериализатор, чтобы User заполнялся автоматически

class MenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Добавляем автоматическое заполнение скрытого поля user именем текущего юзера

    class Meta:
        model = Men
        fields = '__all__'  # Выводим все поля


Для класса MenAPIDestroy установим права IsAdminUser чтобы удалять записи мог только администратор

class MenAPIDestroy(RetrieveDestroyAPIView):  # Класс отвечающий за delete запросы
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    permission_classes = (IsAdminUser, )  # Добавляем права IsAdminUser


Но при этом без права админа мы даже и просмотреть не можем запись. Для этого нужно написать кастомные права.

Создаем в папке приложения файл permissions.py в нем будут все самописные права.


from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):  # Наследуем от базового класса BasePermission
    def has_permission(self, request, view):  # И переопределяем его базовый метод has_permission
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = GET, HEAD, OPTIONS
            return True  # True - разрешено. Даем доступ всем

        return bool(request.user and request.user.is_staff)  # Если не SAFE_METHODS, то только для админа


class IsOwnerOrReadOnly(permissions.BasePermission):  # Наследуем от базового класса BasePermission
    def has_object_permission(self, request, view, obj):  # И переопределяем его базовый метод has_object_permission
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = GET, HEAD, OPTIONS
            return True  # True - разрешено. Даем доступ всем

        return obj.user == request.user  # Если автор записи == текущему юзеру, то тоже возвращаем True и даем доступ



И Теперь мы можем применить самописные права для наших представлений


from .permissions import IsAdminOrReadOnly

class MenAPIDestroy(RetrieveDestroyAPIView):  # Класс отвечающий за delete запросы
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    permission_classes = (IsAdminOrReadOnly, )  # Добавляем самописные права IsAdminOrReadOnly


class MenAPIUpdate(RetrieveUpdateAPIView):  # Класс отвечающий за обработку put и patch (изменение записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    permission_classes = (IsAdminOrReadOnly, )  # Добавляем самописные права IsAdminOrReadOnly



Так же в SETTINGS можем дефолтно определить какие права будут для всех сразу.
Поставим доступ только авторизованным пользователям:

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Определяет что работаем с JSON
        'rest_framework.renderers.BrowsableAPIRenderer',  # Подключаем работу с данными через браузер
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]    
}




**********************************************************************************************************

11. Авторизация и аутентификация. 

Из встроенных методов доступны:

Session-based - аутентификация на основе сессии из cookies
Token-based - аутентификация на основе токенов (библиотека Djoser)

Из сторонних подгружаемых пакетов:

JSON Web Token (JWT) authentication - аутентификация на основе JWT (библиотека Simple JWT)
Django REST framework OAuth - авторизация через социальные сериализатор
И другие...



Session-based authentication:
Для этого типа авторизации достаточно в маршрутах добавить еще один

path('api/v1/drf-auth/', include('rest_framework.urls')),  # маршрут для авторизации

Выдаст ошибку т.к. ждет определенный вариант
http://127.0.0.1:8000/api/v1/drf-auth/login/  --  нас перекинет автоматом в наш аккаунт (но будет ошибка т.к. у нас нет страницы аккаунта). Но теперь можем перейти на http://127.0.0.1:8000/api/v1/men/
или
http://127.0.0.1:8000/api/v1/drf-auth/logout/




**********************************************************************************************************

12. Аутентификация по токенам. Пакет Djoser

Устанавливаем пакет Djoser
pip install djoser


Добавляем его в settings в установленные программы, а так же прописываем разрешение в библиотеки фреймворка на работу с токенами

INSTALLED_APPS = [
    .......

    'rest_framework.authtoken',  # Для стандартной аутентификации по токенам
    'djoser',  # Для аутентификации по токенам с помощью Djoser
]


REST_FRAMEWORK = {
    ......

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Подключаем аутентификацию по токенам
        'rest_framework.authentication.BasicAuthentication',  # Подключаем аутентификацию по логину и паролю (используется DRF по умолчанию)
        'rest_framework.authentication.SessionAuthentication',  # Подключаем аутентификацию по сессиям (используется DRF по умолчанию)
    ],
}


Выполняем миграции

python manage.py migrate


Добавляем новые маршруты для аутентификации в urls

from django.urls import include, path, re_path  # импортируем функцию path для создания маршрутов

path('api/v1/auth/', include('djoser.urls')),  # маршрут для работы с токенами
re_path(r'^auth/', include('djoser.urls.authtoken')),  # маршрут для работы с токенами



Запускаем сервер и теперь по адресу http://127.0.0.1:8000/api/v1/auth/ нам доступна работа с users
Здесь можно содавать новых и менять инфо и состояние текущих пользователей.

Создадим нового в postman
методом POST на адрес http://127.0.0.1:8000/api/v1/auth/users/
Во вкладке Body и Form data:

username: seconduser
password: какой то свой пароль не менее 8 символов и бла бла бла....
email: phk@gmail.com

Если обновим страницу http://127.0.0.1:8000/api/v1/auth/users/ то увидим второго зарегистрированного пользователя

Теперь авторизуемся в системе так же в postman по адресу http://127.0.0.1:8000/auth/token/login/ отправим POST запрос
Так же во вкладке Body и Form data:

username: seconduser
password: какой то свой пароль этого пользователя

После отправки нам выдадут токен и он будет записан в БД именно для этого пользователя.

Теперь для входа в headers сайта необходдимо отправлять этот токен.
Если разлогиниться (так же с участием токена в хедере), то токен стирается из БД и войти с ним уже не получится.
Нужно будет заново отправлять логин и пароль, чтобы получить новый токен.

Так же можно дополнительно ограничивать доступы по токенам.
например

from rest_framework.authentication import TokenAuthentication

class MenAPIUpdate(RetrieveUpdateAPIView):  # Класс отвечающий за обработку put и patch (изменение записей в БД)
    queryset = Men.objects.all()  # Получаем список всех записей из БД и помещаем их в переменную queryset
    serializer_class = MenSerializer  # Указываем какой сериализатор будем использовать
    permission_classes = (IsAuthenticated, )  # Добавляем права IsAuthenticated
    authentication_classes = (TokenAuthentication, )  # Добавляем дополнительно права TokenAuthentication

Здесь дополнительно введена проверка токена. И даже если мы просто авторизовались по сессии, то данные нам не предоставят, т.к. мы не ввели токен.




**********************************************************************************************************

13. Авторизация по JWT-токенам ОБЩАЯ ИНФА

JWT токены состоят из частей разделенных точкой
-Header - Заголовок (json с указанным алгоритмом шифрования и типом токена). Кодируется алгоритмом base64
-Payload - Полезные данные (json с информацией о пользоватле и времени жизни этого JWT токена). Кодируется алгоритмом base64
-Signature - Подпись = складывается из Header и Payload, шифруется указанным в Header алгоритмом


Коротко суть на примере регистрации к сервисам Гугл:
При авторизации юзеру отправляется access_token и refresh_token
access_token отправляется на все сервисы гугла для авторизации, чтобы их все можно было использовать одному юзеру.
Срок жизни таких токенов обычно 5-10 минут.
refresh_token записывается в БД и используется для обновления access_token по истечении жизни access_token.

Т.е на сервер каждые 5-10 минут отправляется запрос и обновляются токены авторизации.
При выходе юзера из учетки и при повторном вводе пароля и логина все повторяется, все токены выдаются новые и по кургу.




**********************************************************************************************************

14. Авторизация по JWT-токенам

Установка библиотеки SimpleJWT

pip install djangorestframework-simplejwt

Добавляем в библиотеку REST_FRAMEWORK

'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Подключаем аутентификацию по JWT токенам
        .....
    ],

Добавляем новые маршруты в urls

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # маршрут для получения токена
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # маршрут для обновления токена
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # маршрут для проверки токена

С официального сайта https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html копируем настройки

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


Переходим по адресу http://127.0.0.1:8000/api/v1/token/
Вводим наши логин и пароль и в ответ получаем access и refresh токены


Теперь пробуем в postman отправить get запрос и получить какую либо запись. Нам ее не дадут.
Переходим во вкладку Header и прописываем
Authorization -> Bearer НАШ_ACCESS_ТОКЕН
Теперь по запросу данные будут предоставлены.

Через какое то время (установленное в настройках. В нашем случеа 5 минут) нам так же откажут в доступе и напишут что токен устарел.

Переходим по адресу http://127.0.0.1:8000/api/v1/token/refresh/ и вставляем наш refresh_token и получаем новый access токен.
Теперь вставив его в header при запросе нам снова дадут доступ на период жизни access токена.