from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import (ProductListView, ContactsPageView, ProductDetailView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryListView)

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='catalog'),
    path('contacts/', cache_page(60)(ContactsPageView.as_view()), name='contacts'),
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),
    path('product/<int:pk>/', ProductDetailView.as_view()),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete')
]
