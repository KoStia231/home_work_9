from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.views import IndexView, ContactsView, ProductView, CategoryView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_info'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category_info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
