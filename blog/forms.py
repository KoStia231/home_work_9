from django import forms

from blog.models import BlogEntry
from catalog.forms import CustomFormMixin, MyCleanForm


class BlogEntryForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма для создания и редактирования записей блога"""

    class Meta:
        model = BlogEntry
        fields = ('title', 'contents', 'image', 'publications')


class BlogEntryModeratorForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма для создания и редактирования записей блога"""

    class Meta:
        model = BlogEntry
        fields = ('publications',)
