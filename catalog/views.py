from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from catalog.models import Product, Category, People


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
    model = People
    fields = ('name', 'phone_number', 'message')
    success_url = reverse_lazy('catalog:contacts')


class IndexView(MyBaseFooter, ListView):
    model = Product
    template_name = 'catalog/index.html'


class ProductView(MyBaseFooter, DetailView):
    model = Product


class CategoryView(MyBaseFooter, DetailView):
    model = Category
