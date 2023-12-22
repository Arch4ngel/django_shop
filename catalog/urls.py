from django.urls import path

from catalog.views import (ProductListView, ContactsPageView, ProductDetailView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView)

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='catalog'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view()),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete')
]
