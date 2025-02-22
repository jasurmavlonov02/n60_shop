from django.shortcuts import render

from shop.models import Product


# Create your views here.


def index(request):
    products = Product.objects.all().order_by('-updated_at')
    context = {
        'products': products
    }
    return render(request, 'shop/home.html', context)


def product_detail(request):
    return render(request, 'shop/detail.html')
