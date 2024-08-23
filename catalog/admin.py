from django.contrib import admin
from .models import Category, Product, People


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'price', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'price',)
    search_fields = ('name', 'description', 'price', 'category', 'created_at', 'updated_at')


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'message')
