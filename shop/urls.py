from django.contrib import admin
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('product/', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products-of-category/<int:category_id>/', views.index, name='products_of_category'),
    path('product-create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product-delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('product-update/<int:product_id>/', views.product_update, name='product_update'),
    path('comment-view/<int:pk>/', views.comment_view, name='comment_view'),
    path('order-view/<int:pk>/', views.order_view, name='order_view')

]
