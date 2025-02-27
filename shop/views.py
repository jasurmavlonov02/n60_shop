from django.shortcuts import render, get_object_or_404

from shop.models import Product, Category


# Create your views here.


def index(request, category_id: int | None = None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all().order_by('-updated_at')  # select * from products order by updated_at DESC
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    # product = Product.objects.get(id=product_id)
    # product = Product.objects.filter(id=product_id).first()

    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'shop/detail.html', context)
