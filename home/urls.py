from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="home"),
    path('view-shop',views.ViewShop,name="shop_page"),
    path('view-subcategory/<int:category_id>/',views.ViewSubcategory,name="sub_category_page"),
    path('display-products/<int:sub_category_id>/',views.DisplayProducts,name="display_product"),
    path('product-details/<int:variant_id>/',views.ProductDetails,name="product_details"),
    path('variant_select/<int:variant_id>/',views.VariantSelect,name="variant_select"),

]

