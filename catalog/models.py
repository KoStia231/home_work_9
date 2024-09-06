from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан в')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлен в')
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.IntegerField(verbose_name='версия')
    name = models.CharField(max_length=200, verbose_name='названии версии')
    is_active = models.BooleanField(default=True, verbose_name='активна')
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор')

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продукта'

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    phone_number = models.IntegerField(verbose_name='телефон')
    message = models.TextField(verbose_name='сообщение')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Contacts(models.Model):
    country = models.CharField(max_length=200, verbose_name='страна')
    inn = models.CharField(verbose_name='инн')
    address = models.TextField(verbose_name='адрес')

    class Meta:
        verbose_name = 'контакт на сайте'
        verbose_name_plural = 'контакты на сайте'

    def __str__(self):
        return self.country

# для себя добавил чтобы не писать ручками)
# python3 manage.py makemigrations
# python3 manage.py migrate
