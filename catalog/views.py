from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from catalog.models import Product, Category


# Create your views here.


def recording_to_file(file_name, data):
    """Запись в файл data.txt это топ задание"""
    with open(file_name, 'a') as file:
        file.write(str(data) + '\n')


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        recording_to_file(file_name="data.txt", data=[name, phone, message])
        # временное решение нужно будет писать потом в базу
        return render(request, self.template_name)


class ProductView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class CategoryView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_list'] = Product.objects.all()
        return context
