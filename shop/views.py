from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'shop/home.html')


def product_detail(request):
    return render(request, 'shop/detail.html')
