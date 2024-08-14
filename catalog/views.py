from django.shortcuts import render

from catalog.models import Product, Category


# Create your views here.


def recording_to_file(file_name, data):
    """Запись в файл data.txt это топ задание"""
    with open(file_name, 'a') as file:
        file.write(str(data)+'\n')


def index(request):
    context = {'product_list': Product.objects.all(), 'category_list': Category.objects.all()}
    return render(request, 'catalog/index.html', context)


def contacts(request):
    context = {'category_list': Category.objects.all()}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        recording_to_file(file_name="data.txt", data=[name, phone, message])
        # временное решение нужно будет писать потом в базу

    return render(request, 'catalog/contacts.html', context)


def product_info(request, pk):
    """Контроллер для отдельной страницы с товаром."""
    context = {'product': Product.objects.get(pk=pk)}
    return render(request, 'catalog/product.html', context)


