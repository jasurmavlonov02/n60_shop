from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('product-detail/',views.product_detail, name='product_detail')

]
