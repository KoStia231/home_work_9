# Учебный интернет магазин

### Для настроек проекта нужно использовать переменные окружения или .env

```
DJANGO_SECRET_KEY='your_secret_key'
DJANGO_DEBUG=True/False
DJANGO_ALLOWED_HOSTS=*/your_host
DB_NAME=name
DB_USER=user
DB_HOST=your_host
DB_PORT=your_port
DB_PASSWORD=password
EMAIL_HOST_USER=your@yandex.ru
EMAIL_HOST_PASSWORD=password
DJANGO_CACHES_ENABLED=True/False
DJANGO_CACHES_LOCATION=your_location
```
###### Пример DJANGO_SECRET_KEY
###### django-insecure-g#ggggg1(%gg&gggg*g1g9g*l1-1@@gggg^!ggg3ggg^!-1g*

### Установить все зависимости 
```python
pip install -r requirements.txt
```

### Создать и применить все миграции
```python
python3 manage.py makemigrations
```
```python
python3 manage.py migrate 
```

### Создать админа
```python
python3 manage.py admin_reg
```
###### Файл для создания админа находится по пути
###### users/management/commands/admin_reg.py


### Наполнить бд товарами
``` python
python3 manage.py loaddata bd.json
```

### Запуск сервера
```python
python3 manage.py runserver 
```
 
## Пользователи в базе

>username-> ***admin@example.com***
> 
>password-> ***admin***

>username-> ***kosta123139@gmail.com***
> 
>password-> ***Hh14767Hh***

