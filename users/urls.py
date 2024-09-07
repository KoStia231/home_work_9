from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import (
    UserLoginView,
    UserRegisterView,
    UserProfileUpdateView,
    UserProfileView,
    verify_mail,
    reset_password
)

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
                  path('', UserLoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', UserRegisterView.as_view(), name='register'),

                  path('profile-update/<int:pk>', UserProfileUpdateView.as_view(), name='profile_update'),
                  path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),

                  path('verify/<str:token>', verify_mail, name='verify'),
                  path('reset_password/', reset_password, name='reset_password'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
