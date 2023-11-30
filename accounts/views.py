import pyotp
from datetime import datetime, timedelta

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
import pyotp
from .models import CustomUser, CustomUserManager
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .utils import  send_otp
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password
# Create your views here.
import re

# view function for user login
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def user_login(request):
    # Check if a user or admin is already logged in
    if 'useremail' in request.session:
        return redirect('home')
    if 'adminemail' in request.session:
        return redirect('admin_home')
    if 'user-email' in request.session:
        del request.session['user-email']
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        # Check if the user exists
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            # Check if the user is blocked
            if not user.is_active:
                messages.error(request, 'Your account has been blocked')
                return redirect('user_login')
                
            # Attempt to authenticate the user
            user = authenticate(request, email=user_email, password=user_password)

            if user is not None and not user.is_superuser:
                # Login the user and set the session variable
                if user.is_verified is True:
                    login(request, user)
                    request.session['useremail'] = user_email
                    return redirect('home')
                else:
                    messages.error(request, 'Please verify your OTP ')
                    request.session['user-email'] = user_email
                    return redirect('send_otp')
            else:
                messages.error(request, 'Email or password is incorrect')
        else:
            messages.error(request, 'User does not exist')

    return render(request, 'accounts/login.html')


# view function for user to signup   
def user_signup(request):

    if request.method == "POST":
        print(request.POST.get('mobile'))
        username = request.POST.get('username')
        user_email = request.POST.get('email')
        phone = request.POST.get('phone_no')
        print("phone_no")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        
       
        email_checking = CustomUser.objects.filter(email = user_email)
        if  email_checking.exists():
            messages.error(request,"email is already taken") 
            return redirect('user_signup')

        
        elif password == confirm_password:
            # otp=send_otp(request,user_email)
            # print(otp,type(otp))

            my_User=CustomUser.objects.create_user(email=user_email,password=password,username=username,phone=phone)
            my_User.save()
            request.session['user-email'] = user_email

            return redirect('send_otp')
        else:
            messages.error( request,'passwords do not match')
            

    return render(request,'accounts/signup.html')

# view function for user to logout
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
# @never_cache
def user_logout(request):
    
    if 'useremail' in request.session:
         
        logout(request)
        
    return redirect('home')

def send_otp(request):
    if 'user-email' in request.session:
        email=request.session['user-email']
        print(email)
    print(',<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    totp=pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp=totp.now()
    request.session['otp_secret_key']= totp.secret
    valid_date=datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date']=str(valid_date)
    
    subject = 'verify your email to continue to create an account at watchhub'
    message = otp
    from_email = settings.EMAIL_HOST_USER   
    recipient_list = [ email ] 
    send_mail(subject, message, from_email, recipient_list)  

    user=CustomUser.objects.get(email=email)
    user.otp=otp
    user.save()
    print(otp,type(otp))
    return redirect('user_otp')


# view function for otp verification of the user after signing up 
@never_cache
def otp_verification(request):
    if 'useremail' in request.session:
        return redirect('homepage')
    if request.method=='POST':
        otp=request.POST.get('otp')
        print(otp)

        
        if 'user-email' in request.session:
            user_email=request.session['user-email']
        
        user=CustomUser.objects.get(email=user_email)
        actual_otp=user.otp
        otp_secret_key=request.session['otp_secret_key']
        otp_valid_date=request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until =datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
               totp=pyotp.TOTP(otp_secret_key,interval=60)

               if actual_otp == int(otp) :

                    # my_User=CustomUser.objects.create_user(email=user_email,password=password,username=username,phone=phone)
                    # my_User.save()
                    user.is_verified=True
                    user.save()
                    
                    del request.session['user-email'] 
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']


                    messages.success(request, 'Account created successfully.')

                    return redirect('user_login')
               else:
                    messages.error(request,"entered otp is not correct!!!")
                    # return redirect('')
                   
            else:
                del request.session['user-email'] 
                # del request.session['username']
                # del request.session['phoneno']
                # del request.session['password']
                del request.session['otp_secret_key']
                del request.session['otp_valid_date']
                messages.error(request,"time expired for otp validation!!!!")

        else:
            messages.error(request,"Something Went wrong")

    return render(request,'accounts/verify.html')


# view function for resending the otp  
def otp_resend(request):
    if 'otp_secret_key' in request.session:
        del request.session['otp_secret_key']
    if 'otp_valid_date' in request.session:
        del request.session['otp_valid_date']

    return redirect('send_otp')

