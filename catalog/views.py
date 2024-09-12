from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView,
    DetailView, DeleteView,
    UpdateView
)

from catalog.models import (
    Product, Category,
    People, Contacts,
    Version
)

from catalog.forms import (
    CategoryForm, ProductForm,
    VersionForm, ProductModeratorForm
)
from catalog.services import get_cache_method_all
from config.settings import CACHES_ENABLED


# Create your views here.


class MyLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для всех страниц, которые требуют авторизации"""
    login_url = 'users:login'
    redirect_field_name = "redirect_to"


class MyBaseFooter:
    """Класс для выноса переопределения функции чтобы в футере была инфа динамически
       не придумал как по другому это сделать класс сам по себе ничего не делает
       просто существует для наследования чтобы пере-определить этот метод у других классов"""

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Список категорий в нижней части сайта он кешируется через сервисную функцию
        context_data['category_list'] = get_cache_method_all(key=f'category_list', models=Category)
        return context_data


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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=True)
        return queryset


class ModeratorView(MyLoginRequiredMixin, PermissionRequiredMixin, MyBaseFooter, ListView):
    """Главная каталога"""
    permission_required = 'catalog.can_edit_description'
    model = Product
    template_name = 'catalog/index_moderator.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=False)
        return queryset


class VersionCreateView(MyLoginRequiredMixin, MyBaseFooter, CreateView):
    """Страничка создания новой версии продукта"""
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'

    def form_valid(self, form):
        """Сохранение версии с автором"""
        version = form.save(commit=False)
        version.autor = self.request.user
        version.save()

        return super().form_valid(form)


class VersionUpdateView(MyLoginRequiredMixin, MyBaseFooter, Version, UpdateView):
    """Страничка редактирования версии продукта"""
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'

    def form_valid(self, form):
        """Сохранение версии с автором"""
        version = form.save(commit=False)
        version.autor = self.request.user
        version.save()

        return super().form_valid(form)


class VersionDeleteView(MyLoginRequiredMixin, MyBaseFooter, DeleteView):
    """Страничка удаления версии продукта"""
    model = Version
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'

    def get_object(self, queryset=None):
        """Проверка, что удаляемая версия создана текущем пользователем"""
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            raise Http404("У вас нет прав на удаление этой версии.")
        return obj


class ProductDetailView(MyBaseFooter, DetailView):
    """Отображение одного продукта"""
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['version'] = Version.objects.filter(product=product, is_active=True).first()
        return context


class ProductCreateView(MyLoginRequiredMixin, MyBaseFooter, CreateView):
    """Страничка создания нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'

    def form_valid(self, form):
        """Сохранение продукта с автором"""
        product = form.save(commit=False)
        product.autor = self.request.user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(MyLoginRequiredMixin, MyBaseFooter, UpdateView):
    """Страничка редактирования продукта"""
    model = Product
    success_url = reverse_lazy('catalog:detail')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('catalog:detail', args=[self.object.pk])

    def get_form_class(self):
        """Редактирование формы для продукта в зависимости от того,
           какие права доступа у текущего пользователя"""
        user = self.request.user
        if user == self.object.autor:
            return ProductForm

        if user.has_perm('catalog.can_edit_description'):
            return ProductModeratorForm
        raise PermissionDenied("У вас нет прав на редактирование этого продукта")


class ProductDeleteView(MyLoginRequiredMixin, MyBaseFooter, DeleteView):
    """Страничка удаления продукта"""
    model = Product
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'

    def get_object(self, queryset=None):
        """Проверка, что удаляемый продукт создан текущем пользователем"""
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            raise Http404("У вас нет прав на удаление этого продукта.")
        return obj


class CategoryDetailView(MyBaseFooter, DetailView):
    """Одна категория со всеми товарами"""
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # (object)_set динамическая переменная которая выводит все продукты из этой категории
        context['products'] = self.object.product_set.filter(publications=True)
        return context


class CategoryCreateView(MyLoginRequiredMixin, MyBaseFooter, CreateView):
    """Страничка создания новой категории"""
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'

    def form_valid(self, form):
        """Сохранение категории с автором"""
        category = form.save(commit=False)
        category.autor = self.request.user
        category.save()

        return super().form_valid(form)


class CategoryUpdateView(MyLoginRequiredMixin, MyBaseFooter, UpdateView):
    """Страничка редактирования категории"""
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_detail')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('catalog:category_detail', args=[self.object.pk])


class CategoryDeleteView(MyLoginRequiredMixin, MyBaseFooter, DeleteView):
    """Страничка удаления категории"""
    model = Category
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'

    def get_object(self, queryset=None):
        """Проверка, что удаляемая категория создана текущем пользователем"""
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            raise Http404("У вас нет прав на удаление этой категории.")
        return obj
