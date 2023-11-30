from django.shortcuts import render,redirect
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q
from categories.models import *
from accounts.models import CustomUser
from store.models import Product,Variation



# Create your views here.
def home(request):

    if 'adminmail' in request.session:
        return redirect('admin_home')
    


    return render(request,'home/home.html')      


def ViewShop(request):
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    variants=Variation.objects.order_by('product').distinct('product')

    available_colours = Variation.objects.filter(is_available=True).values('color').distinct()
    context={
        'category':categories,
        'product':products,
        'variants':variants,
        'color':available_colours

    }


    return render(request,'home/shop.html',context)

def ViewSubcategory(request,category_id):
    variants={}
    subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    # Assuming you already have 'subcategory' containing the filtered subcategories
    variants = Variation.objects.filter(product_sub_category_in=subcategory)


    context={
        'subcategory':subcategory,
        'base_variant':variants
    }

    return render(request,'subcategory.html',context)


def DisplayProducts(request,sub_category_id):
    
    product = Product.objects.filter(Q(is_activate=True) & Q(sub_category = sub_category_id))
    variants = Variation.objects.filter(product_sub_category_in=subcategory)    
    

    context={
        'variants':variants
            
            }                            
    return render(request,'products_display.html',context)

def ProductDetails(request,variant_id):

    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id)

    context={
        # 'product':product,
        'variant': variants,
        'available_variants':available_variants
    }
    return render(request, 'home/product_details.html', context)