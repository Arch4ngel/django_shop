from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from catalog.models import Product

# Create your views here.


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Каталог'}


class ContactsPageView(View):
    def get(self, request):
        context = {'title': 'Контакты'}
        return render(request, 'catalog/contacts.html', context)

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')
        context = {'title': 'Контакты'}
        return render(request, 'catalog/contacts.html', context)


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['title'] = product.name
        return context
