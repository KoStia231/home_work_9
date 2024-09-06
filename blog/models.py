from django.db import models


# Create your models here.
class BlogEntry(models.Model):
    """Модель блога"""
    title = models.CharField(max_length=50, verbose_name='название')
    slug = models.CharField(max_length=200)
    contents = models.TextField(verbose_name='содержимое')
    publications = models.BooleanField(default=True, verbose_name='флаг публикации')
    image = models.ImageField(upload_to='blog_entry/', verbose_name='превью')
    views = models.IntegerField(default=0, verbose_name='просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    autor = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='автор')

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

    def __str__(self):
        return self.title
