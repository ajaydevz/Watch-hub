from django.urls import path
from . import views



urlpatterns = [
    
       
       path('',views.CartPage,name='cart_page'),
       path('add-cart/<int:product_id>/',views.AddCart,name='add_cart'),
       path('increment-cart/<int:product_id>/',views.IncrementCartitem,name="increment_cartitem"),
       path('decrement-cart/<int:product_id>/',views.DecrementCartitem,name="decrement_cartitem"),
       path('remove-cart-item/<int:product_id>/',views.RemoveCartItem,name="remove_cartitem"),
       path('address-checkout',views.AddressCheckout,name="address_checkout"),
       path('add-address-checkout/<int:user_id>/',views.AddAddressCheckout,name="add_address_checkout"),
       path('checkout',views.CheckoutPage,name="checkout_page"),
       path('order',views.PlaceOrder,name='place_order'),
       path('order-success',views.OrderSuccess,name='order_success'),
]