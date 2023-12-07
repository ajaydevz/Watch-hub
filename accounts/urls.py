from django.urls import path
from . import views

urlpatterns = [

    path('user-login',views.UserLogin,name="user_login"),
    path('user-signup',views.UserSignup,name="user_signup"),
    path('user-logout',views.UserLogout,name='user_logout'),

    path('send-otp',views.SendOtp,name='send_otp'),
    path('user-otp',views.OtpVerification,name='user_otp'),
    path('user-resend-otp',views.OtpResend,name='user_otp_resend'),

    path('user-forgot-pass',views.ForgotPass,name='forgot_pass'),
    path('user-reset-pass',views.ResetPass,name= 'reset_pass'),
    path('user-forgot-pass-otp',views.ForgotPassOtp, name= "forgot_pass_otp"),

     
]
