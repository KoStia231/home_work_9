from django.contrib.auth.forms import UserCreationForm
from auth_users.models import User

from catalog.forms import CustomFormMixin, MyCleanForm


class RegisterForm(UserCreationForm, CustomFormMixin, MyCleanForm):
    # Наследуемся от специальной формы UserCreationForm из модуля auth
    class Meta:
        model = User
        # Указываем новую кастомную модель
        fields = ('email', 'password1', 'password2', 'avatar', 'phone_number', 'country')
        # Меняем поля, так как исходная форма UserCreationForm
        # ссылается на поле username
