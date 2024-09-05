from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from auth_users.views import RegisterView

from auth_users.apps import AuthUsersConfig

app_name = AuthUsersConfig.name

urlpatterns = [
                  path('', RegisterView.as_view(), name='register'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
