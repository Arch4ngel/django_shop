from django.urls import path

from catalog.views import ProductListView, ContactsPageView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view()),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view())
]
