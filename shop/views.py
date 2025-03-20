from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from shop.models import Product, Category
from shop.forms import ProductModelForm, CommentModelForm, OrderModelForm
from django.db.models import Avg

from django.core.paginator import Paginator


# Create your views here.


def index(request, category_id: int | None = None):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()
    filter_query = request.GET.get('filter', '')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all().order_by('-updated_at')  # select * from products order by updated_at DESC

    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if filter_query == 'expensive':
        products = products.order_by('-price')

    elif filter_query == 'cheap':
        products = products.order_by('price')

    elif filter_query == 'rating':
        products = products.annotate(rating_avg=Avg('comments__rating')).order_by('-rating_avg')

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.all().annotate(rating_avg=Avg('comments__rating')).filter(
        category=product.category).exclude(id=product.id).order_by('-rating_avg')
    comments = product.comments.all()
    context = {
        'product': product,
        'categories': categories,
        'comments': comments,
        'related_products': related_products
    }
    return render(request, 'shop/detail.html', context)


# @login_required(login_url='/admin/')
# def product_create(request):
#     form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     context = {
#         'form': form
#     }
#     return render(request, 'shop/product-create.html', context)

# @login_required(login_url='/admin/')
# def product_create(request):
#     form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#
#             return redirect('index')
#
#     context = {
#         'form': form,
#         'action': 'Create'
#     }
#     return render(request, 'shop/product-create.html', context)
class ProductCreateView(CreateView):
    model = Product
    template_name = 'shop/product-create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('shop:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def get_success_url(self):
        #email logic
        pass



@login_required(login_url='/admin/')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id)
    context = {
        'product': product,
        'form': form,
        'action': 'Update'
    }
    return render(request, 'shop/product-update.html', context)


@login_required(login_url='/admin/')
def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if product:
        product.delete()
        return redirect('index')
    return render(request, 'shop/detail.html', {'product': product})


def comment_view(request, pk):
    product = Product.objects.get(id=pk)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            rating = request.POST.get('rating')
            print(type(rating))
            comment.rating = rating
            comment.product = product
            comment.save()
            return redirect('product_detail', product.id)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)


def order_view(request, pk):
    product = Product.objects.get(id=pk)
    form = OrderModelForm()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        quantity = int(request.POST.get('quantity'))
        if form.is_valid():
            if product.quantity >= quantity:
                order = form.save(commit=False)
                order.product = product
                product.quantity = product.quantity - quantity
                product.save()
                order.save()
                # message success
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Order successfully created'
                )
                return redirect('product_detail', product.id)
            else:
                # error message
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Something is wrong'
                )
    return render(request, 'shop/detail.html', {'form': form, 'product': product})
