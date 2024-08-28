from django import forms

from blog.models import BlogEntry


class BlogEntryForm(forms.ModelForm):
    """Форма для создания и редактирования записей блога"""
    class Meta:
        model = BlogEntry
        fields = ('title', 'contents', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    WORDS = (
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    )

    def clean_title(self):
        """Проверка на наличие запрещенных слов в названии"""
        cleaned_data = self.cleaned_data.get('title')

        if cleaned_data.lower() in self.WORDS:
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова в названии')

        return cleaned_data

    def clean_contents(self):
        """Проверка на наличие запрещенных слов в тексте"""
        cleaned_data = self.cleaned_data.get('contents')

        if cleaned_data.lower() in self.WORDS:
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова в тексте')

        return cleaned_data

