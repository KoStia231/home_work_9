# Учебный интернет магазин

### Для настроек проекта нужно использовать переменные окружения

###### пример файла .env

```
.env.example
```

### Установить все зависимости

```python
pip install - r requirements.txt
```

### Создать и применить все миграции

```python
python3
manage.py
makemigrations
```

```python
python3
manage.py
migrate 
```

### Создать админа

```python
python3
manage.py
admin_reg
```

###### Файл для создания админа находится по пути

###### users/management/commands/admin_reg.py

### Наполнить бд товарами

``` python
python3 manage.py loaddata bd.json
```

### Запуск сервера

```python
python3
manage.py
runserver 
```

## Пользователи в базе

> username-> ***admin@example.com***
>
>password-> ***admin***

> username-> ***kosta123139@gmail.com***
>
>password-> ***Hh14767Hh***

