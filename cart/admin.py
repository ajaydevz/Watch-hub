from django.contrib import admin
from .models import CartItem,Cart, Order, OrderItem
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)