from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from store.models import Variation
from .models import WishlistItem
from django.contrib import messages


# Create your views here.
def wishlist(request):
    if request.user:
        user = request.user

    wishlist_items = WishlistItem.objects.filter(user=user)
    context = {"wishlist": wishlist_items}

    return render(request, "userprofile/wishlist.html", context)


@login_required(login_url="user_login")
def add_to_wishlist(request, product_id):
    variant = Variation.objects.get(id=product_id)
    print(variant.id)
    user = request.user
    print(user.email)
    try:
        is_exist = WishlistItem.objects.filter(user=user, product_name=variant).exists()

        if is_exist:
            # Wishlist item already exists
            messages.error(request, "This product is already in your wishlist.")
            return redirect("product_details", variant_id=variant.id)
        else:
            # Wishlist item does not exist, add it
            wishlist = WishlistItem(user=user, product_name=variant)
            wishlist.save()
            # messages.success(request, 'Product added to wishlist.')
            return redirect("wishlist_view")

    except Exception as e:
        # Handle exceptions if any
        # Log or handle the exception accordingly
        print(e)
        messages.error(request, "Failed to add the product to the wishlist.")
        return redirect("wishlist_view")


def remove_wish_list(request, product_id):
    wishlist_item = None  # Initializing the variable
    try:
        product = Variation.objects.get(id=product_id)
        # Find the wishlist item
        wishlist_item = WishlistItem.objects.get(
            product_name=product, user=request.user
        )
        wishlist_item.delete()  # Remove the wishlist item
    except WishlistItem.DoesNotExist:
        pass
    wishlist = WishlistItem.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist,
    }
    return render(request, "userprofile/wishlist.html", context)
