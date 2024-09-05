from django.shortcuts import render
from django.views.generic import CreateView

from auth_users.forms import RegisterForm
from auth_users.models import User


class RegisterView(CreateView):
    """Страничка регистрации нового пользователя"""
    model = User
    form_class = RegisterForm





# Create your views here.
