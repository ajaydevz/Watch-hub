from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import CustomUser, CustomUserManager
import pyotp
import random
import json
import string
from .utils import send_otp
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from accounts.models import UserWallet
from datetime import datetime
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def UserLogin(request):
    print("__________________________")
    print("__________________________")
    print("__________________________")
    print("__________________________")

    print("__________________________")
    print("__________________________")
    print("__________________________")
    print("__________________________")
    print("__________________________")

    # Check if a user or admin is already logged in
    if "useremail" in request.session:
        return redirect("home")
    if "adminemail" in request.session:
        return redirect("admin_home")
    if "user-email" in request.session:
        del request.session["user-email"]
    if request.method == "POST":
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")

        # Check if the user exists
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            # Check if the user is blocked
            if not user.is_active:
                messages.error(request, "Your account has been blocked")
                return redirect("user_login")

            # Attempt to authenticate the user
            user = authenticate(request, email=user_email, password=user_password)

            if user is not None and not user.is_superuser:
                # Login the user and set the session variable
                if user.is_verified is True:
                    login(request, user)
                    request.session["useremail"] = user_email
                    return redirect("home")
                else:
                    messages.error(request, "Please verify your OTP ")
                    request.session["user-email"] = user_email
                    return redirect("send_otp")
            else:
                messages.error(request, "Email or password is incorrect")
        else:
            messages.error(request, "User does not exist")

    return render(request, "accounts/login.html")


def UserSignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user_email = request.POST.get("email")
        phone = request.POST.get("phone_no")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmpassword")
        ref_code = request.POST.get("referral_code")

        if ref_code:
            try:
                referrer = CustomUser.objects.get(referral_code=ref_code)
                referrer.wallet = referrer.wallet + 100
                referrer.save()
                wallerhistory_referer = UserWallet(user=referrer)
                wallerhistory_referer.transaction = "Credit"
                wallerhistory_referer.created_at = datetime.now()
                wallerhistory_referer.amount = 100

                wallerhistory_referer.save()

            except CustomUser.DoesNotExist:
                referrer = None
        else:
            referrer = None

        # checking the email is valid or not
        email_checking = CustomUser.objects.filter(email=user_email)
        if email_checking.exists():
            messages.error(request, "email is already taken")
            return redirect("user_signup")

        elif password == confirm_password:
            my_User = CustomUser.objects.create_user(
                email=user_email, password=password, username=username, phone=phone
            )
            my_User.referral_code = generate_referral_code()
            my_User.referrer = referrer
            my_User.save()
            request.session["user-email"] = user_email

            payhis = CustomUser.objects.get(email=user_email)
            payhis.referrer

            if payhis.referrer:
                payhis.wallet = payhis.wallet + 100
                payhis.save()

                wallerhistory = UserWallet(user=payhis)
                wallerhistory.transaction = "Credit"
                wallerhistory.created_at = datetime.now()
                wallerhistory.amount = 100
                wallerhistory.save()

            return redirect("send_otp")
        else:
            messages.error(request, "passwords do not match")

    return render(request, "accounts/signup.html")


def generate_referral_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def UserLogout(request):
    if "useremail" in request.session:
        # Log out the user and flush the session.
        logout(request)
        # Debugging output
        print("User has been logged out")

        # Flush the session to ensure the user is logged out and clear any stored session data.
    request.session.flush()

    return redirect("home")


def SendOtp(request):
    if "user-email" in request.session:
        email = request.session["user-email"]
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session["otp_secret_key"] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session["otp_valid_date"] = str(valid_date)

    subject = "verify your email to continue to create an account "
    message = otp
    from_email = settings.EMAIL_HOST_USER
    
   
    print("__________________")
    print("The email is the ", request.session["user-email"])
    print("__________________")
    

    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    user = CustomUser.objects.get(email=email)
    user.otp = otp
    user.save()
    print(otp, type(otp))
    return redirect("user_otp")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def OtpVerification(request):
    if "useremail" in request.session:
        return redirect("home")
    if request.method == "POST":
        otp = request.POST.get("otp")
        print(otp)

        if "user-email" in request.session:
            user_email = request.session["user-email"]

        user = CustomUser.objects.get(email=user_email)
        actual_otp = user.otp
        otp_secret_key = request.session["otp_secret_key"]
        otp_valid_date = request.session["otp_valid_date"]

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)

                if actual_otp == int(otp):
                    user.is_verified = True
                    user.save()

                    del request.session["user-email"]
                    del request.session["otp_secret_key"]
                    del request.session["otp_valid_date"]

                    messages.success(
                        request, "Successfully verified OTP. You can now log in."
                    )

                    return redirect("user_login")
                else:
                    messages.error(request, "entered otp is not correct!!!")

            else:
                del request.session["otp_secret_key"]
                del request.session["otp_valid_date"]
                messages.error(request, "time expired for otp validation!!!!")

        else:
            messages.error(request, "Something Went wrong")

    return render(request, "accounts/verify.html")


# view function for resending the otp


def OtpResend(request):
    # deleting the session of existing one time password
    try:
        del request.session["otp_secret_key"]
        del request.session["otp_valid_date"]
    except:
        pass
    return redirect("send_otp")


def ForgotPass(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print(email)
        if CustomUser.objects.filter(email=email).exists():
            # user=CustomUser.objects.get(email=email)
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp = totp.now()
            request.session["otp_secret_key"] = totp.secret
            valid_date = datetime.now() + timedelta(minutes=1)
            request.session["otp_valid_date"] = str(valid_date)

            subject = "verify your email to continue to create an account at watchhub"
            message = otp
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            user = CustomUser.objects.get(email=email)
            user.otp = otp
            user.save()
            request.session["check_mail"] = email
            return redirect("forgot_pass_otp")
        else:
            messages.error(request, "There is no account linked with this email")
            return redirect("forgot_pass")

    return render(request, "accounts/forgotpass.html")


# function for validating the otp


def ForgotPassOtp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        if "check_mail" in request.session:
            email = request.session["check_mail"]
        user = CustomUser.objects.get(email=email)
        actual_otp = user.otp
        otp_secret_key = request.session["otp_secret_key"]
        otp_valid_date = request.session["otp_valid_date"]

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)

                if actual_otp == int(otp):
                    #    del request.session['check_mail']
                    del request.session["otp_valid_date"]
                    del request.session["otp_secret_key"]

                    return redirect("reset_pass")
                else:
                    messages.error(request, "OTP you have enterd is incorrect")
                    return redirect("forgot_pass_otp")
            else:
                messages.error(request, "Time limit exceeded")

                del request.session["check_mail"]
                del request.session["otp_valid_date"]
                del request.session["otp_secret_key"]
                return redirect("forgot_pass_otp")

    return render(request, "accounts/forgotpass_verify.html")


# function for reseting the password


def ResetPass(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            email = request.session["check_mail"]
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(
                    password1
                )  # Use set_password to hash and set the password
                user.save()
                del request.session["check_mail"]
                return redirect("user_login")
            except CustomUser.DoesNotExist:
                messages.error(request, "There is no account linked with this email")
                del request.session["check_mail"]
                return redirect("reset_pass")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "accounts/reset_pass.html")
