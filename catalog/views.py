from django.shortcuts import render
from catalog.models import Category, Product

# Create your views here.


def catalog(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Каталог'
    }
    return render(request, 'catalog/templates/index.html', context)


def contacts(request):
    context = {'title': 'Контакты'}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')
    return render(request, 'catalog/templates/contacts.html', context)


def product_info(request, pk):
    product = Product.objects.get(pk=pk)

    context = {
        'object': product,
        'title': product.name,
        'category': product.category
    }
    return render(request, 'catalog/templates/product-info.html', context)

# def categories(request):
#     context = {
#         'object_list': Category.objects.all(),
#         'title': 'Продукты'
#     }
#     return render(request, 'main/category_list.html', context)
