# Учебный интернет магазин

### Для настройки базы данных и почтового сервиса нужно создать файл .env

```
DB_NAME=name
DB_USER=user
DB_PASSWORD=password
EMAIL_HOST_USER=your@yandex.ru
EMAIL_HOST_PASSWORD=password
```

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

