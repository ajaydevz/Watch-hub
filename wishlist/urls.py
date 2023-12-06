from django.urls import path
from . import views


urlpatterns = [
    path('',views.wishlist,name="wishlist_view"),
    path('add-to-wishlist<int:product_id>',views.add_to_wishlist,name="add_to_wishlist"),
    path('remove-from-wishlist<int:product_id>',views.remove_wish_list,name="remove_wishlist")

]