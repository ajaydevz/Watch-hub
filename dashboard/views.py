from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser, UserWallet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from cart.models import Order, OrderItem
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.utils.datetime_safe import datetime
from django.http import HttpResponse
from store.models import Coupon
from django.http import StreamingHttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from categories.models import Category, Sub_Category
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage



# Create your views here.
@cache_control(no_store=True, no_cache=True)
def AdminLogin(request):
    if "useremail" in request.session:
        return redirect("user_login")

    if "adminmail" in request.session:
        return redirect("admin_home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            request.session["adminmail"] = email
            return redirect("admin_home")
        else:
            messages.error(request, "Invalid credentials try again !!")

    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    return render(request, "dashboard/adminlogin.html")


@staff_member_required(login_url="admin_login")
@cache_control(no_store=True, no_cache=True)
def AdminHome(request):
    if "adminmail" in request.session:
        users_active = CustomUser.objects.filter(is_active=True).count()
        users_block = CustomUser.objects.filter(is_active=False).count()
        orders_delevered = Order.objects.filter(status="Delevered").count()
        orders_confirmed = Order.objects.filter(status="Order confirmed").count()
        orders_cancelled = Order.objects.filter(status="Cancelled").count()
        orders_returned = Order.objects.filter(status="Returned").count()
        orders = Order.objects.all()
        orders_count = Order.objects.all().count()
        total_sales = 0
        for order in orders:
            total_sales = total_sales + order.total_price
        print(total_sales)
        print(total_sales)
        print(int(total_sales))

        revenue = 0

        context = {
            "orders_delevered": orders_delevered,
            "orders_confirmed": orders_confirmed,
            "orders_cancelled": orders_cancelled,
            "orders_returned": orders_returned,
            "users_active": users_active,
            "users_block": users_block,
            "total_sales": total_sales,
            "orders_count": orders_count,
        }
        return render(request, "dashboard/adminhome.html", context)


def AdminLogout(request):
    if "adminmail" in request.session:
        logout(request)
        return redirect("admin_login")
    else:
        return redirect(request, "dashboard/adminlogin.html")


# view function for going to user page
@staff_member_required(login_url="admin_login")
def Users(request):
    user_page = 10

    users = CustomUser.objects.filter(is_superuser=False).order_by("id")

    paginator =Paginator(users,user_page)
    page = request.GET.get('page',1)

    try:
        users = paginator.page(page)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {"users": users}
    return render(request, "dashboard/users.html", context)


# view function for blocking and unblocking the users
def BlockUser(request, user_id):
    user = CustomUser.objects.get(pk=user_id)

    if user.is_active:
        user.is_active = False
        user.save()
        users = CustomUser.objects.filter(is_superuser=False).order_by("id")

        context = {"users": users}

        return render(request, "dashboard/users.html", context)

    else:
        user.is_active = True
        user.save()
        users = CustomUser.objects.filter(is_superuser=False).order_by("id")
        context = {"users": users}
        return render(request, "dashboard/users.html", context)


@staff_member_required(login_url="admin_login")
def Categories(request):
    category = Category.objects.all().order_by("id")
    context = {"categories": category}

    return render(request, "dashboard/category.html", context)


def AddCategories(request):
    if request.method == "POST":
        category_name = request.POST.get("categoryName")
        category_desc = request.POST.get("categoryDescription")
        category_image = request.FILES.get("category_img")
        category_offer = request.POST.get("category_offer")

        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, "Cannot Add An Existing Category !!")
            return redirect("categories")
        else:
            category = Category(
                category_name=category_name,
                description=category_desc,
                category_image=category_image,
                category_offer=category_offer,
            )
            category.save()
            return redirect("categories")


def EditCategories(request, category_id):
    category = Category.objects.get(id=category_id)
    category_image = category.category_image
    if request.method == "POST":
        category_name = request.POST.get("categoryName")

        category.description = request.POST.get("categoryDescription")
        category_img = request.FILES.get("category_img")

        if category_img is None:
            category.category_image = category_image

        else:
            category.category_image = category_img

        if "category_offer" in request.POST:
            category_offer = request.POST["category_offer"]

            try:
                # Try to convert the value to a number
                category_offer = int(category_offer)
            except ValueError:
                messages.error(request, "Category offer must be a number.")
                return redirect("categories")

            category.category_offer = category_offer

        category.save()

        if (
            Category.objects.filter(category_name=category_name)
            .exclude(id=category_id)
            .exists()
        ):
            messages.error(request, "Entered Category is already taken!!")
            return redirect("categories")

        else:
            category.category_name = category_name
            category.save()
            return redirect("categories")


def DeleteCategories(request, category_id):
    category = Category.objects.get(pk=category_id)

    if category.is_activate:
        category.is_activate = False
        category.save()

        category = Category.objects.all().order_by("id")
        context = {"categories": category}
        return render(request, "dashboard/category.html", context)
    else:
        category.is_activate = True
        category.save()
        category = Category.objects.all().order_by("id")
        context = {"categories": category}
        return render(request, "dashboard/category.html", context)


# View for displaying subcategories


@staff_member_required(login_url="admin_login")
def SubCategories(request):
    # Fetch active categories from the database
    category = Category.objects.filter(is_activate=True)
    # Fetch all subcategories and order them by their ID
    subcategory = Sub_Category.objects.all().order_by("id")
    context = {"subcategories": subcategory, "categories": category}
    return render(request, "dashboard/subcategories.html", context)


# View for adding subcategories
def AddSubCategories(request):
    if request.method == "POST":
        # Get the selected category's ID from the form
        category_id = request.POST.get("category_name")
        # Retrieve the selected category instance
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get("categoryName")
        description = request.POST.get("categoryDescription")
        cat_image = request.FILES.get("cat_img")
        cat = Sub_Category(
            category=category_instance,
            sub_category_name=sub_category_name,
            sub_category_description=description,
            sub_Category_image=cat_image,
        )
        cat.save()
        return redirect("sub_categories")


# View for editing subcategories
def EditSubCategories(request, subcategory_id):
    subcategory = Sub_Category.objects.get(pk=subcategory_id)
    # Fetch the image from the database for when the user hasn't edited the image field
    sub_category_image = subcategory.sub_Category_image

    if request.method == "POST":
        # Get the selected category's ID from the form
        category_id = request.POST.get("category_name")
        # Update the category field of the subcategory using the selected category ID
        subcategory.category = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get("categoryName")
        subcategory.sub_category_name = sub_category_name
        subcategory.sub_category_description = request.POST.get("categoryDescription")

        sub_Category_img = request.FILES.get("cat_img")
        # Check if the subcategory image is None
        if sub_Category_img is None:
            subcategory.sub_Category_image = sub_category_image
        else:
            subcategory.sub_Category_image = sub_Category_img

        # Check if the new subcategory name is already taken
        if (
            Sub_Category.objects.filter(sub_category_name=sub_category_name)
            .exclude(id=subcategory_id)
            .exists()
        ):
            messages.error(request, "Entered Sub Category is already taken!!")
            return redirect("sub_categories")
        else:
            subcategory.save()
            return redirect("sub_categories")


# View for activating or deactivating subcategories
def DeleteSubCategories(request, subcategory_id):
    category = Sub_Category.objects.get(pk=subcategory_id)

    if category.is_activate:
        category.is_activate = False
    else:
        category.is_activate = True

    category.save()

    # Fetch active categories and all subcategories, ordering them by ID
    categories = Category.objects.filter(is_activate=True).order_by("id")
    subcategories = Sub_Category.objects.all().order_by("id")
    context = {"subcategories": subcategories, "categories": categories}
    return render(request, "dashboard/subcategories.html", context)


@staff_member_required(login_url="admin_login")
def Orders(request):
    orders = Order.objects.all().order_by("created_at")

    order_items = OrderItem.objects.order_by("order").distinct("order")

    for order in orders:
        print("this is my payment status", order.payment_mode)
    context = {"orders": orders, "orderitems": order_items}
    return render(request, "dashboard/orders.html", context)


@staff_member_required(login_url="admin_login")
def OrdersDetails(request, order_id):
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)

    context = {"order": order, "orderitems": order_item}

    return render(request, "dashboard/orders_details.html", context)


def OrderStatus(request):
    if request.method == "POST":
        url = request.META.get("HTTP_REFERER")
        try:
            order_id = request.POST.get("order_id")
            order_status = request.POST.get("order_status")
            print(order_status)
            if order_status == "Order Status":
                order = Order.objects.get(id=order_id)
                order_item = OrderItem.objects.filter(order=order)
                context = {"order": order, "order_item": order_item}
                return redirect(url)
            order = Order.objects.get(id=order_id)
            order_item = OrderItem.objects.filter(order=order)

            order.status = order_status
            order.save()
            if order_status == "Returned" or order_status == "Cancelled":
                if (
                    order.payment_mode == "Paid by Razorpay"
                    or order.payment_mode == "wallet"
                ):
                    email = order.user.email
                    user = CustomUser.objects.get(email=email)
                    user.wallet = user.wallet + order.total_price
                    userwallet = UserWallet()
                    userwallet.user = user
                    userwallet.amount = order.total_price
                    userwallet.transaction = "Credited"
                    userwallet.save()
                    user.save()

                order_item.save()

            order_item = OrderItem.objects.filter(order=order)
            context = {"order": order, "order_item": order_item}
            print(order.total_price)
            print("order_status")
            return redirect(url)

        except:
            pass
    print("order_status")
    order_item = OrderItem.objects.filter(order=order)
    context = {"order": order, "order_item": order_item}

    return render(request, "dashboard/orders_details.html", context)


def GetSalesRevenue(request):
    total_sales = 0
    if request.method == "POST":
        users = CustomUser.objects.filter(is_active=True).count()
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        print(start_date)
        request.session["start_date"] = start_date
        request.session["end_date"] = end_date


        if start_date == end_date:
            print(start_date)
            orders = Order.objects.filter(created_at__date=start_date)
        else:
            orders = Order.objects.filter(created_at__range=(start_date, end_date))
        total_order = Order.objects.filter(
            created_at__range=(start_date, end_date)
        ).count()
        Pending = Order.objects.filter(
            created_at__range=(start_date, end_date), status="Order confirmed"
        ).count()
        Processing = Order.objects.filter(
            created_at__range=(start_date, end_date), status="In Production"
        ).count()
        Shipped = Order.objects.filter(
            created_at__range=(start_date, end_date), status="Shipped"
        ).count()
        Delivered = Order.objects.filter(
            created_at__range=(start_date, end_date), status="Delivered"
        ).count()
        cancelled = Order.objects.filter(
            created_at__range=(start_date, end_date), status="Cancelled"
        ).count()
        Return = Order.objects.filter(
            created_at__range=(start_date, end_date), status="Returned"
        ).count()

        for order in orders:
            total_sales = total_sales + order.total_price

        context = {
            "users": users,
            # 'total':total,
            "orders": orders,
            "total_sales": total_sales,
            "total_order": total_order,
            "Pending": Pending,
            "Processing": Processing,
            "Shipped": Shipped,
            "Delivered": Delivered,
            "cancelled": cancelled,
            "Return": Return,
            "sales": Delivered,
            "cancelled": cancelled,
            # "returned":returned,
            # 'monthly_sales_data': monthly_sales_data
        }
        return render(request, "dashboard/sales_revenue.html", context)

    else:
        orders = Order.objects.all()
        total_order = Order.objects.all().count()
        Pending = Order.objects.filter(status="Order confirmed").count()
        Processing = Order.objects.filter(status="In Production").count()
        Shipped = Order.objects.filter(status="Shipped").count()
        Delivered = Order.objects.filter(status="Delivered").count()
        cancelled = Order.objects.filter(status="Cancelled").count()
        Return = Order.objects.filter(status="Returned").count()
        for order in orders:
            total_sales = total_sales + order.total_price

        if "adminmail" in request.session:
            current_year = timezone.now().year

            # Calculate monthly sales for the current year
            monthly_sales = (
                Order.objects.filter(created_at__year=current_year)
                .annotate(month=ExtractMonth("created_at"))
                .values("month")
                .annotate(total_sales=Sum("total_price"))
                .order_by("month")
            )

            # Create a dictionary to hold the monthly sales data
            monthly_sales_data = {month: 0 for month in range(1, 13)}

            for entry in monthly_sales:
                month = entry["month"]
                total_sales = entry["total_sales"]
                monthly_sales_data[month] = total_sales
            users = CustomUser.objects.all().count()
            try:
                sales = Order.objects.filter(status="Delivered").count()
                revenue = Order.objects.filter(status="Delivered")
                total = 0
                for i in revenue:
                    total += i.total_price
            except:
                sales = 0
            try:
                cancelled = Order.objects.filter(status="Cancelled").count()
            except:
                cancelled = 0
            try:
                returned = Order.objects.filter(status="Returned").count()
            except:
                returned = 0

            context = {
                "users": users,
                "total": total,
                "orders": orders,
                "total_sales": total_sales,
                "total_order": total_order,
                "Pending": Pending,
                "Processing": Processing,
                "Shipped": Shipped,
                "Delivered": Delivered,
                "cancelled": cancelled,
                "Return": Return,
                "sales": sales,
                "cancelled": cancelled,
                "returned": returned,
                "monthly_sales_data": monthly_sales_data,
            }
            return render(request, "dashboard/sales_revenue.html", context)
        else:
            return redirect("admin_login")


def RenderToPdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Sales_report.pdf"'

    # Create a PDF with xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


def SalesReportPdfDownload(request):
    if "start_date" and "end_date" in request.session:
        start_date = request.session["start_date"]
        end_date = request.session["end_date"]
        try:
            order = Order.objects.filter(created_at__range=(start_date, end_date))
            del request.session["start_date"]
            del request.session["end_date"]
        except:
            order = None
    else:
        order = Order.objects.all()
    context = {
        "orders": order,
        "start_date": start_date,
        "end_date": end_date,
    }
    pdf = RenderToPdf("dashboard/sales_report_pdf.html", context)
    return pdf


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin, login_url="admin_login")
def coupon(request):
    coupon = Coupon.objects.all().order_by("id")

    context = {
        "coupon": coupon,
    }
    return render(request, "dashboard/coupon.html", context)


def add_coupon(request):
    if request.method == "POST":
        coupon_name = request.POST.get("couponName")
        coupon_code = request.POST.get("couponCode")
        discountAmount = request.POST.get("discountAmount")
        validFrom = request.POST.get("validFrom")
        validTo = request.POST.get("validTo")
        minimumAmount = request.POST.get("minimumAmount")

        if Coupon.objects.filter(coupon_name=coupon_name).exists():
            messages.error(request, "Entered Coupon is already exists!!")
            return redirect("coupon")
        elif Coupon.objects.filter(code=coupon_code).exists():
            messages.error(request, "Entered Coupon code is already exists!!")
            return redirect("coupon")

        else:
            coupon = Coupon(
                coupon_name=coupon_name,
                code=coupon_code,
                discount=discountAmount,
                valid_from=validFrom,
                valid_to=validTo,
                minimum_amount=minimumAmount,
            )
            coupon.save()

            return redirect("coupon")


def edit_coupon(request, coupon_id):
    if request.method == "POST":
        coupon = Coupon.objects.get(id=coupon_id)

        coupon_name = request.POST.get("couponName")
        coupon.coupon_name = coupon_name

        coupon_code = request.POST.get("couponCode")
        coupon.coupon_code = request.POST.get("couponCode")

        coupon.discount = request.POST.get("discountAmount")
        coupon.valid_from = request.POST.get("validFrom")
        coupon.valid_to = request.POST.get("validTo")
        coupon.minimum_amount = request.POST.get("minimumAmount")

        if (
            Coupon.objects.filter(coupon_name=coupon_name)
            .exclude(id=coupon_id)
            .exists()
        ):
            messages.error(request, "Coupon name you have chosen is already taken ")
            return redirect("coupon")

        elif Coupon.objects.filter(code=coupon_code).exclude(id=coupon_id).exists():
            messages.error(request, "Coupon code you have chosen is already taken ")
            return redirect("coupon")

        else:
            coupon.save()
            return redirect("coupon")


def block_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    print("hihihihjihihihihihihihiii")
    if coupon.is_available == True:
        coupon.is_available = False
    else:
        coupon.is_available = True
    coupon.save()
    return redirect("coupon")
