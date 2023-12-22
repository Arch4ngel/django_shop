from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version

# Create your views here.


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')


class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Каталог'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            active_version = product.version_set.filter(is_active=True).first()
            if active_version:
                product.active_version_number = active_version.number
                product.active_version_name = active_version.name
            else:
                product.active_version_number = None
                product.active_version_name = None

        return context


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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    extra_context = {'title': 'Удалить пост'}
    success_url = reverse_lazy('catalog:catalog')
