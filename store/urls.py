# from django.urls import path
# from . import views
# from .views import variant_view


# urlpatterns = [
#     path('delete-products/<int:product_id>/', views.DeleteProduct, name="delete_product"),
#     path('', views.product_view, name="product_view"),
#     path('add-products', views.AddProduct, name="add_product"),
#     path('edit-products/<int:product_id>/', views.EditProduct, name="edit_product"),
#     path('variant/<int:product_id>/', variant_view, name='variant_view'),
#     path('add_variant/<int:product_id>/', views.add_variant, name='add_variant'),

# ]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductView, name="product_view"),
    path("add-products", views.AddProduct, name="add_product"),
    path("edit-products/<int:product_id>/", views.EditProduct, name="edit_product"),
    path(
        "delete-products/<int:product_id>/", views.DeleteProduct, name="delete_product"
    ),
    path("view-varirants/<int:product_id>/", views.VariantView, name="variant_view"),
    path("add-varirants/<int:product_id>/", views.AddVariant, name="add_variant"),
    path("edit-varirants/<int:variant_id>/", views.EditVariants, name="edit_variants"),
    path(
        "delete-varirants/<int:variant_id>/",
        views.DeleteVariant,
        name="delete_variants",
    ),
]
