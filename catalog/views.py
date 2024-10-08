from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView,
    DetailView, DeleteView,
    UpdateView
)

from catalog.forms import (
    CategoryForm, ProductForm,
    VersionForm, ProductModeratorForm
)
from catalog.models import (
    Product, Category,
    People, Contacts,
    Version
)


# Create your views here.


class MyLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для всех страниц, которые требуют авторизации"""
    login_url = 'users:login'
    redirect_field_name = "redirect_to"


class ContactsView(CreateView):
    """Отображение странички контактов и
    формы сбора контактов от пользователя с последующим сохранением в бд"""
    model = People
    fields = ('name', 'phone_number', 'message')
    success_url = reverse_lazy('catalog:contacts')

    @staticmethod
    def view_contacts():
        return Contacts.objects.all()


class IndexView(ListView):
    """Главная каталога"""
    model = Product
    template_name = 'catalog/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=True)
        return queryset


class ModeratorView(MyLoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Главная каталога"""
    permission_required = 'catalog.can_edit_description'
    model = Product
    template_name = 'catalog/index_moderator.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=False)
        return queryset


class VersionlistView(MyLoginRequiredMixin, DetailView):
    """Страница со списком версий продукта"""
    model = Product
    template_name = 'catalog/version_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['version_list'] = Version.objects.filter(product=product)
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверка, что пользователь является автором версии
        if obj.autor != self.request.user:
            raise Http404("Вы не являетесь автором этой версии продукта")
        return obj


class VersionCreateView(MyLoginRequiredMixin, CreateView):
    """Страничка создания новой версии продукта"""
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:version_list')
    template_name = 'catalog/object_form.html'

    def get_form_kwargs(self):
        """Чтобы закрепить версию к продукту в форме"""
        kwargs = super().get_form_kwargs()
        product_pk = self.request.GET.get('product_pk')
        kwargs['initial'] = {'product': product_pk}
        return kwargs

    def form_valid(self, form):
        """Сохранение версии с автором"""
        version = form.save(commit=False)
        version.autor = self.request.user
        version.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на страницу со списком версий после создания новой версии"""
        return reverse('catalog:version_list', args=[self.object.product.pk])


class VersionUpdateView(MyLoginRequiredMixin, UpdateView):
    """Страничка редактирования версии продукта"""
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:version_list')
    template_name = 'catalog/object_form.html'

    def form_valid(self, form):
        """Сохранение версии с автором"""
        version = form.save(commit=False)
        version.autor = self.request.user
        version.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на страницу со списком версий после редактирования версии"""
        return reverse('catalog:version_list', args=[self.object.product.pk])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверка, что пользователь является автором версии
        if obj.autor != self.request.user:
            raise Http404("Вы не являетесь автором этой версии продукта")
        return obj


class VersionDeleteView(MyLoginRequiredMixin, DeleteView):
    """Страничка удаления версии продукта"""
    model = Version
    success_url = reverse_lazy('catalog:version_list')
    template_name = 'catalog/object_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверка, что пользователь является автором версии
        if obj.autor != self.request.user:
            raise Http404("Вы не являетесь автором этой версии продукта")
        return obj

    def get_success_url(self):
        """Перенаправление на страницу продукта после удаления версии"""
        return reverse('catalog:version_list', args=[self.object.product.pk])


class ProductDetailView(DetailView):
    """Отображение одного продукта"""
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['version'] = Version.objects.filter(product=product, is_active=True).last()
        return context


class ProductCreateView(MyLoginRequiredMixin, CreateView):
    """Страничка создания нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_detail')
    template_name = 'catalog/object_form.html'

    def form_valid(self, form):
        """Сохранение продукта с автором"""
        product = form.save(commit=False)
        product.autor = self.request.user
        product.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        category_pk = self.request.GET.get('category_pk')
        kwargs['initial'] = {'category': category_pk}
        return kwargs

    def get_success_url(self):
        """Перенаправление на страницу категории после создания продукта"""
        return reverse('catalog:category_detail', args=[self.object.category.pk])


class ProductUpdateView(MyLoginRequiredMixin, UpdateView):
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


class ProductDeleteView(MyLoginRequiredMixin, DeleteView):
    """Страничка удаления продукта"""
    model = Product
    success_url = reverse_lazy('catalog:category_detail')
    template_name = 'catalog/object_confirm_delete.html'

    def get_object(self, queryset=None):
        """Проверка, что удаляемый продукт создан текущем пользователем"""
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            raise Http404("У вас нет прав на удаление этого продукта.")
        return obj

    def get_success_url(self):
        """Перенаправление на страницу категории после создания продукта"""
        return reverse('catalog:category_detail', args=[self.object.category.pk])


class CategoryDetailView(DetailView):
    """Одна категория со всеми товарами"""
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # (object)_set динамическая переменная которая выводит все продукты из этой категории
        context['products'] = self.object.product_set.filter(publications=True)
        return context


class CategoryCreateView(MyLoginRequiredMixin, CreateView):
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


class CategoryUpdateView(MyLoginRequiredMixin, UpdateView):
    """Страничка редактирования категории"""
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_detail')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('catalog:category_detail', args=[self.object.pk])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверка, что пользователь является автором версии
        if obj.autor != self.request.user:
            raise Http404("Вы не являетесь автором этой категории")
        return obj


class CategoryDeleteView(MyLoginRequiredMixin, DeleteView):
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
