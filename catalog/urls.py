from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import (
    IndexView, ModeratorView, ContactsView, ProductDetailView,
    CategoryDetailView, ProductUpdateView, ProductDeleteView,
    ProductCreateView, CategoryUpdateView, CategoryDeleteView,
    CategoryCreateView, VersionCreateView, VersionUpdateView,
    VersionDeleteView
)
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('product-not-publications/', ModeratorView.as_view(), name='moderator'),
                  path('product/<int:pk>/', cache_page(300)(ProductDetailView.as_view()), name='detail'),
                  path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
                  path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
                  path('product/create/', ProductCreateView.as_view(), name='create'),

                  path('product/version/create/', VersionCreateView.as_view(), name='create_version'),
                  path('product/version/update/<int:pk>/', VersionUpdateView.as_view(), name='update_version'),
                  path('product/version/delete/<int:pk>/', VersionDeleteView.as_view(), name='delete_version'),

                  path('contacts/', cache_page(300)(ContactsView.as_view()), name='contacts'),

                  path('category/<int:pk>/', cache_page(300)(CategoryDetailView.as_view()), name='category_detail'),
                  path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
                  path('category/delete//<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
                  path('category/create/', CategoryCreateView.as_view(), name='category_create'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
