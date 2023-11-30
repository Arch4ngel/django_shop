from django.urls import path

from catalog.views import catalog, contacts, product_info

app_name = 'catalog'

urlpatterns = [
    path('', catalog),
    path('contacts/', contacts),
    path('product/<int:pk>/', product_info)
]
