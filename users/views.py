from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from config.settings import EMAIL_HOST_USER
import secrets


class UserRegisterView(CreateView):
    """Страничка регистрации нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/registr.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка пользователю письма с подтверждением регистрации"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/verify/{token}'
        send_mail(
            subject=f'Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def verify_mail(request, token):
    """Страничка подтверждения регистрации переход по ссылке из письма и редирект на страницу входа"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserProfileView(UpdateView):
    """Страничка редактирования профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

# Create your views here.
