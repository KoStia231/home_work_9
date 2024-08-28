from django import forms

from catalog.models import Product, Category


class MyClean():
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
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова в названии')

        return cleaned_data

    def clean_description(self):
        """Проверка поля 'description' на наличие запрещенных"""
        cleaned_data = self.cleaned_data.get('description')

        if cleaned_data.lower() in self.WORDS:
            raise forms.ValidationError('Ошибка, нельзя использовать эти слова в описании')

        return cleaned_data


class ProductForm(MyClean, forms.ModelForm):
    """Форма создания и редактирования продукта"""
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CategoryForm(MyClean, forms.ModelForm):
    """Форма создания и редактирования категории"""

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
