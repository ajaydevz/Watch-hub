from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from cart.models import Order,OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from categories.models import Category,Sub_Category


# Create your views here.

@cache_control(no_store=True, no_cache=True)

def AdminLogin(request):
    if 'adminmail' in request.session :
        return redirect ('admin_home')
    
    if request.method =="POST":
        email = request.POST.get('email')
        password= request.POST.get('password')

        user= authenticate(request, email= email , password= password )
        if user is not None and user.is_superuser:
            login(request,user)
            request.session['adminmail']= email
            return redirect('admin_home')
        else:
            messages.error(request,"Invalid credentials try again !!")

    print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    return render(request,"dashboard/adminlogin.html")


def AdminHome (request):
    user_acive = CustomUser.objects.filter(is_active=True).count()
    user_blocked = CustomUser.objects.filter(is_active=False).count()
    context={
        'user_active':user_acive,
        'user_blocked':user_blocked
          
       }
    
    return render(request, 'dashboard/admin_base.html',context)





def AdminLogout(request):

    if 'adminmail' in request.session :
        logout(request)
        return redirect('admin_login')
    else:
        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        return redirect(request,'dashboard/admin_login.html')

 
   
    
#view function for going to user page 
def Users(request):
    user = CustomUser.objects.filter(is_superuser= False).order_by('id')

    context= {
        'users': user
    }
    return render (request, 'dashboard/users.html',context)


#view function for blocking and unblocking the users
def BlockUser(request, user_id):

    user=CustomUser.objects.get(pk=user_id)
    
    if user.is_active:
        user.is_active=False
        user.save()
        users=CustomUser.objects.filter(is_superuser= False).order_by('id')

        context={
         
            'users':users
        
        }

        return render(request,'dashboard/users.html',context)
    
    else:
        user.is_active=True
        user.save()
        users= CustomUser.objects.filter(is_superuser=False).order_by('id')
        context = {
            'users' : users
        }
        return render(request,'dashboard/users.html',context)




def Categories(request):

    category = Category.objects.all().order_by('id')
    context={
        'categories' : category 
    }

    return render(request,'dashboard/category.html',context)


def AddCategories(request):

    if request.method == 'POST':
        category_name = request.POST.get('categoryName')
        category_desc = request.POST.get('categoryDescription')
        category_image = request.FILES.get('category_img')

        if Category.objects.filter(category_name = category_name).exists():
            messages.error(request, "Cannot Add An Existing Category !!")
            return redirect('categories')
        else:
            category = Category(category_name= category_name, description = category_desc , category_image= category_image)
            category.save()
            return redirect('categories') 
        
        
def EditCategories(request,category_id):
    category = Category.objects.get(id=category_id)
    category_image=category.category_image
    if request.method=="POST":
        category_name= request.POST.get('categoryName')
        
        category.description    = request.POST.get('categoryDescription')
        category_img = request.FILES.get('category_img')

        if category_img is None:
            category.category_image = category_image
    
        else:
            category.category_image = category_img

        if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
            messages.error(request,"Entered Category is already taken!!")
            return redirect('categories')
            
        else:
             category.category_name  = category_name
             category.save()
             return redirect('categories')
        

def DeleteCategories(request,category_id):
    category=Category.objects.get(pk=category_id)

    if category.is_activate:
        category.is_activate=False
        category.save()

       
    
        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/category.html',context)
    else:
        category.is_activate=True
        category.save()
        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/category.html',context)
    

# View for displaying subcategories
def SubCategories(request):
    # Fetch active categories from the database
    category = Category.objects.filter(is_activate=True)
    # Fetch all subcategories and order them by their ID
    subcategory = Sub_Category.objects.all().order_by('id')
    context = {
        'subcategories': subcategory,
        'categories': category
    }
    return render(request, 'dashboard/subcategories.html', context)


# View for adding subcategories
def AddSubCategories(request):
    if request.method == "POST":
        # Get the selected category's ID from the form
        category_id = request.POST.get('category_name')
        # Retrieve the selected category instance
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('categoryName')
        description = request.POST.get('categoryDescription')
        cat_image = request.FILES.get('cat_img')
        cat = Sub_Category(
            category=category_instance,
            sub_category_name=sub_category_name,
            sub_category_description=description,
            sub_Category_image=cat_image
        )
        cat.save()
        return redirect('sub_categories')


# View for editing subcategories
def EditSubCategories(request, subcategory_id):
    subcategory = Sub_Category.objects.get(pk=subcategory_id)
    # Fetch the image from the database for when the user hasn't edited the image field
    sub_category_image = subcategory.sub_Category_image

    if request.method == "POST":
        # Get the selected category's ID from the form
        category_id = request.POST.get('category_name')
        # Update the category field of the subcategory using the selected category ID
        subcategory.category = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('categoryName')
        subcategory.sub_category_name = sub_category_name
        subcategory.sub_category_description = request.POST.get('categoryDescription')

        sub_Category_img = request.FILES.get('cat_img')
        # Check if the subcategory image is None
        if sub_Category_img is None:
            subcategory.sub_Category_image = sub_category_image
        else:
            subcategory.sub_Category_image = sub_Category_img

        # Check if the new subcategory name is already taken
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=subcategory_id).exists():
            messages.error(request, "Entered Sub Category is already taken!!")
            return redirect('sub_categories')
        else:
            subcategory.save()
            return redirect('sub_categories')


# View for activating or deactivating subcategories
def DeleteSubCategories(request, subcategory_id):
    category = Sub_Category.objects.get(pk=subcategory_id)

    if category.is_activate:
        category.is_activate = False
    else:
        category.is_activate = True

    category.save()

    # Fetch active categories and all subcategories, ordering them by ID
    categories = Category.objects.filter(is_activate=True).order_by('id')
    subcategories = Sub_Category.objects.all().order_by('id')
    context = {
        'subcategories': subcategories,
        'categories': categories
    }
    return render(request, 'dashboard/subcategories.html', context)




def Orders(request):

    orders = Order.objects.all()
    order_items = OrderItem.objects.order_by('order').distinct('order')
    
    for order in orders:
        print('this is my payment status',order.payment_mode)
    context={
        "orders":orders,
        "orderitems":order_items
    }
    return render(request,"dashboard/orders.html",context)



def OrdersDetails(request,order_id):
    
    order=Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)

    context={
        "order":order,
        "orderitems":order_item
    }

    return render(request,"dashboard/orders_details.html",context)



def OrderStatus(request):
    # Handle updating order status
    if request.method == 'POST':
        # Get the URL of the previous page
        url = request.META.get('HTTP_REFERER')
        try:
            # Get order_id and order_status from the form
            order_id = request.POST.get('order_id')
            order_status = request.POST.get('order_status')
            
            # Check if the order status is 'Order Status'
            if order_status == 'Order Status':
                # Retrieve order and order items
                order = Order.objects.get(id=order_id)
                order_item = OrderItem.objects.filter(order=order)
                # Prepare context and redirect to the previous page
                context = {
                    'order': order,
                    'order_item': order_item
                }
                return redirect(url)

            # Continue with updating order status
            order = Order.objects.get(id=order_id)
            order_item = OrderItem.objects.filter(order=order)
            
            # Update order status
            order.status = order_status
            order.save()

            # Retrieve order items and prepare context
            order_item = OrderItem.objects.filter(order=order)
            context = {
                'order': order,
                'order_item': order_item
            }

            # Print order details for debugging
            print(order.total_price)
            print("order_status")

            # Redirect to the previous page
            return redirect(url)
         
        except:
            pass

    # If not a POST request, render the order details page
    print("order_status")
    order_item = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_item': order_item
    }
    return render(request, 'dashboard/orders_details.html', context)
