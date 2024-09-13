from django import forms

from catalog.models import Product, Category, Version


class CustomFormMixin:
    """Стилизация внешнего вида формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MyCleanForm:
    """Форматирование полей формы чтобы нельзя было добавить слова из списка, клас используется для наследования"""
    WORDS = (
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    )

    def clean_name(self):
        """Проверка поля 'name' на наличие запрещенных слов"""
        cleaned_data = self.cleaned_data.get('name').lower()
        for word in self.WORDS:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка, нельзя использовать эти слова')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description').lower()
        for word in self.WORDS:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка, нельзя использовать эти слова')
        return cleaned_data

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title').lower()
        for word in self.WORDS:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка, нельзя использовать эти слова')
        return cleaned_data


class ProductForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования продукта"""

    class Meta:
        model = Product
        exclude = ('autor',)


class ProductModeratorForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования продукта модератора"""

    class Meta:
        model = Product
        fields = ('publications', 'description', 'category',)


class CategoryForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования категории"""

    class Meta:
        model = Category
        exclude = ('autor',)


class VersionForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования версии продукта"""

    class Meta:
        model = Version
        exclude = ('autor',)
        widgets = {
            'product': forms.HiddenInput(),
        }
