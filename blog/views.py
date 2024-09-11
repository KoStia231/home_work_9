from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404

from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from blog.forms import (
    BlogEntryForm, BlogEntryModeratorForm
)
from catalog.views import (
    MyBaseFooter, MyLoginRequiredMixin
)
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)
from blog.models import BlogEntry


class BlogIndexView(MyBaseFooter, ListView):
    """Отображение главной страницы блога"""
    model = BlogEntry
    template_name = 'blog/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=True)
        return queryset


class ModeratorView(MyLoginRequiredMixin, PermissionRequiredMixin, MyBaseFooter, ListView):
    """Отображение главной страницы блога"""
    permission_required = 'blog.can_edit_publications'
    model = BlogEntry
    template_name = 'blog/index_moderator.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=False)
        return queryset


class BlogDetailView(MyBaseFooter, DetailView):
    """Отображение одной записи блога"""
    model = BlogEntry
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object


class BlogCreateView(MyLoginRequiredMixin, MyBaseFooter, CreateView):
    """Страничка с созданием записи блога"""
    model = BlogEntry
    form_class = BlogEntryForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        """Сохранение новой записи с автором и слагом"""
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.autor = self.request.user
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(MyLoginRequiredMixin, MyBaseFooter, UpdateView):
    """Старничка с редактированием блога """
    model = BlogEntry

    success_url = reverse_lazy('blog:detail')

    def form_valid(self, form):
        """Сохранение новой записи с и слагом"""
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', args=[self.object.slug])

    def get_form_class(self):
        """Определяет вид формы для редактирования"""
        user = self.request.user
        if user == self.object.autor:
            return BlogEntryForm
        if user.has_perm('blog.can_edit_publications'):
            return BlogEntryModeratorForm
        raise PermissionDenied("У вас нет прав на редактирование этого прод")


class BlogDeleteView(MyLoginRequiredMixin, MyBaseFooter, DeleteView):
    """Страничка с удалением блога"""
    model = BlogEntry
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        """Проверка, что удаляемая статья создана текущем пользователем"""
        obj = super().get_object(queryset)

        if obj.autor != self.request.user:
            raise Http404("У вас нет прав на удаление этой статьи .")
        return obj
# Create your views here.
