from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from users.views import (
    UserRegisterView,
    UserProfileView,
    verify_mail
)

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
                  path('', LoginView.as_view(template_name='users/login.html'), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', UserRegisterView.as_view(), name='register'),
                  path('profile/', UserProfileView.as_view(), name='profile'),
                  path('verify/<str:token>', verify_mail, name='verify'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
