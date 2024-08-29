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
        """Проверка поля 'name' на наличие запрещенных"""
        cleaned_data = self.cleaned_data.get('name')
        if cleaned_data.lower() in self.WORDS:
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        if cleaned_data.lower() in self.WORDS:
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова')
        return cleaned_data

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title')
        if cleaned_data.lower() in self.WORDS:
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова')
        return cleaned_data


class ProductForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования продукта"""
    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования категории"""
    class Meta:
        model = Category
        fields = '__all__'


class VersionForm(CustomFormMixin, MyCleanForm, forms.ModelForm):
    """Форма создания и редактирования версии продукта"""
    class Meta:
        model = Version
        fields = '__all__'


