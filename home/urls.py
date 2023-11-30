from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('view-shop',views.ViewShop,name="shop_page"),
    path('display-products/',views.DisplayProducts,name="display_product"),
    path('product-details/<int:variant_id>/',views.ProductDetails,name="product_details"),
    

]


