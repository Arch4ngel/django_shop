from django.urls import path

from catalog.views import catalog, contacts

app_name = 'catalog'

urlpatterns = [
    path('', catalog),
    path('contacts/', contacts)
]
