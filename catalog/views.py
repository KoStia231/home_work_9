from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from catalog.models import Product, Category, People, Contacts


# Create your views here.


class MyBaseFooter:
    """Класс для выноса переопределения функции чтобы в футере была инфа динамически
       не придумал как по другому это сделать класс сам по себе ничего не делает
       просто существует для наследования чтобы пере-определить этот метод у других классов"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_list'] = Product.objects.all()
        return context


class ContactsView(MyBaseFooter, CreateView):
    """Отображение странички контактов и
    формы сбора контактов от пользователя с последующим сохранением в бд"""
    model = People
    fields = ('name', 'phone_number', 'message')
    success_url = reverse_lazy('catalog:contacts')

    @staticmethod
    def view_contacts():
        return Contacts.objects.all()


class IndexView(MyBaseFooter, ListView):
    """Главная каталога"""
    model = Product
    template_name = 'catalog/index.html'


class ProductDetailView(MyBaseFooter, DetailView):
    """Отображение одного продукта"""
    model = Product


class ProductCreateView(MyBaseFooter, CreateView):
    """Страничка создания нового продукта"""
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'


class ProductUpdateView(MyBaseFooter, UpdateView):
    """Страничка редактирования продукта"""
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('catalog:detail')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('catalog:detail', args=[self.object.pk])


class ProductDeleteView(MyBaseFooter, DeleteView):
    """Страничка удаления продукта"""
    model = Product
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'


class CategoryDetailView(MyBaseFooter, DetailView):
    """Одна категория со всеми товарами в ней реализованно через класс MyBaseFooter"""
    model = Category


class CategoryCreateView(MyBaseFooter, CreateView):
    """Страничка создания новой категории"""
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'


class CategoryUpdateView(MyBaseFooter, UpdateView):
    """Страничка редактирования категории"""
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('catalog:category_detail')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('catalog:category_detail', args=[self.object.pk])


class CategoryDeleteView(MyBaseFooter, DeleteView):
    """Страничка удаления категории"""
    model = Category
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'
