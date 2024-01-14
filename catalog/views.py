from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.http import Http404

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version

# Create your views here.


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permissin_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def test_func(self):
        _user = self.request.user
        _instance: Product = self.get_object()
        custom_perms: tuple = (
            'catalog_app.set_publication',
            'catalog_app.set_category',
            'catalog_app.set_description',
        )

        if _user == _instance.user:
            return True
        elif _user.groups.filter(name='moder') and _user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.user = self.request.user
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    extra_context = {'title': 'Удалить пост'}
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:catalog')
