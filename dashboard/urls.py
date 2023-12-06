from django.urls import path
from . import views


urlpatterns = [


       path('',views.AdminLogin,name='admin_login'),
       path('admin_home/',views.AdminHome,name='admin_home'),
       path('admin_logout/',views.AdminLogout,name='admin_logout'),
       path('users/',views.Users,name='users'),
       path('block/<int:user_id>/',views.BlockUser,name='block_user'),
       
       path('categories/',views.Categories,name='categories'),
       path('add_categories/',views.AddCategories,name='add_categories'),
       path('edit_categories/<int:category_id>/',views.EditCategories,name='edit_categories'),
       path('delete_categories/<int:category_id>/',views.DeleteCategories,name='delete_categories'),
       path('sub-categories/',views.SubCategories,name='sub_categories'),
       path('add-subcategories/',views.AddSubCategories,name='add_subcategories'),
       path('edit-subcategories/<int:subcategory_id>/',views.EditSubCategories,name='edit_subcategories'),
       path('delete-subcategories/<int:subcategory_id>/',views.DeleteSubCategories,name='delete_subcategories'),

       path('orders',views.Orders,name="orders"),
       path("orders-details/<int:order_id>/",views.OrdersDetails,name="orders_details"),
       path('order-status',views.OrderStatus,name="order_status"),

]