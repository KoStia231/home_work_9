from django.shortcuts import render

# Create your views here.


def recording_to_file(file_name, data):
    """Запись в файл data.txt это топ задание"""
    with open(file_name, 'a') as file:
        file.write(str(data)+'\n')


def index(request):
    return render(request, 'catalog/index.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        recording_to_file(file_name="data.txt", data=[name, phone, message])

    return render(request, 'catalog/contacts.html')



