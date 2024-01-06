from decimal import Decimal
import os
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from store.models import Product,Variation
from categories.models import Category,Sub_Category
from django.contrib import messages
# Create your views here.



def ProductView(request):
    if 'adminmail' in request.session:
        products = Product.objects.all()
        categories = Category.objects.filter(is_activate=True)
        sub_categories = Sub_Category.objects.filter(is_activate=True)

        context={
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
        
        return render(request,'dashboard/products.html',context)
    else:
        return redirect('admin_login')
    
def AddProduct(request):
     product = Product()
     if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('product_description')
        sub_category = request.POST.get('subcategory_name')
        sub_cat = Sub_Category.objects.get(id=sub_category)
        product.sub_category = sub_cat
        product.category = sub_cat.category
      
        product.save()
            
        return redirect('product_view')
       

def EditProduct(request,product_id):
    product=Product.objects.get(pk = product_id)

    if request.method == 'POST':
        product_name = request.POST['product_name']
        product.product_name = request.POST['product_name']
        product.description = request.POST['product_description']
        sub_category_id = request.POST.get('subcategory_name')
        sub_category_instance=Sub_Category.objects.get(pk=sub_category_id)
        product.category=sub_category_instance.category
       
        
        if Product.objects.filter(product_name=product_name).exclude(pk=product_id).exists():

            messages.error(request,"Entered product already Exists")
            return redirect('sub_categories')
        else:
            product.save()
            return redirect('product_view')
        
def DeleteProduct(request,product_id):
     product=Product.objects.get(pk=product_id)

     if product.is_activate:
        product.is_activate=False
        product.save()

       
        
        products = Product.objects.all()
        categories = Category.objects.filter(is_activate=True)
        sub_categories = Sub_Category.objects.filter(is_activate=True)

        context={
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
        return render(request,'dashboard/products.html',context)
     
    
     else:
        product.is_activate=True
        product.save()
        
        products = Product.objects.all()
        categories = Category.objects.filter(is_activate=True)
        sub_categories = Sub_Category.objects.filter(is_activate=True)

        context={
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
        }
        return render(request,'dashboard/products.html',context)

@staff_member_required(login_url='admin_login')
def VariantView(request,product_id):

    variants = Variation.objects.filter(product=product_id)
    product = Product.objects.get(pk=product_id)
    
    context = {
       
       'variant': variants,
       'product': product,
    }

    return render(request, 'dashboard/variants.html',context)


def AddVariant(request,product_id):
    product_id = product_id
    if request.method =='POST':
        product = Product.objects.get(pk=product_id)
        color = request.POST.get('color')
        stock = request.POST.get('stock')
        actual_price = request.POST.get('ActualPrice')
        selling_price = request.POST.get('SellingPrice')
        images = request.FILES.getlist('VariantImage')
        image1 = images[0]
        image2 = images[1]
        image3 = images[2]
        image4 = images[3]
        
        variant = Variation(
            product = product,
            color = color,
            stock = stock,
            actual_price = actual_price,
            selling_price = selling_price,
            # assigning the images into the single variables
            image1 = image1,
            image2 = image2,
            image3 = image3,
            image4 = image4

        )
        variant.save()

        return redirect('variant_view',product_id)



def EditVariants(request, variant_id):
    variant = get_object_or_404(Variation, pk=variant_id)
    product_id = variant.product.id

    if request.method == 'POST':
        # Update the Variation object with new data
        variant.color = request.POST.get('color')
        variant.stock = request.POST.get('stock')
        variant.actual_price = request.POST.get('ActualPrice')
        variant.selling_price = request.POST.get('SellingPrice')
        
        # Handle image uploads
        images = request.FILES.getlist('VariantImage')
        for i in range(min(len(images), 4)):
            image_field_name = f'image{i+1}'  # image1, image2, image3, image4
            image = images[i]
            setattr(variant, image_field_name, image)

        # Delete existing image files only if new images are uploaded
        if any(images):
            if variant.image1 and os.path.exists(variant.image1.path):
                os.remove(variant.image1.path)
            if variant.image2 and os.path.exists(variant.image2.path):
                os.remove(variant.image2.path)
            if variant.image3 and os.path.exists(variant.image3.path):
                os.remove(variant.image3.path)
            if variant.image4 and os.path.exists(variant.image4.path):
                os.remove(variant.image4.path)

        variant.save()
        return redirect('variant_view',product_id)



def DeleteVariant(request,variant_id):
    variant = get_object_or_404(Variation, pk=variant_id)
    product_id = variant.product.id
    if variant.is_available:
        variant.is_available=False
        variant.save()

    else:
        variant.is_available=True
        variant.save()
    return redirect('variant_view',product_id)