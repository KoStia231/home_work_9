from django.contrib import admin

from .models import (
    Category, Product,
    People, Contacts, Version
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'name', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'price', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'price',)
    search_fields = ('name', 'description', 'price', 'category', 'created_at', 'updated_at')


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'message')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('country', 'inn', 'address')

    # Это чтобы нельзя было создать больше одной сущности контакты
    def save_model(self, request, obj, form, change):
        # Проверяем, если уже есть объект в базе данных
        if Contacts.objects.exists():
            # Если есть, то не сохраняем новый объект
            return
        # Если нет, сохраняем новый объект
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Переопределяем метод удаления объекта
        super().delete_model(request, obj)
