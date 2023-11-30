import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import CustomUser

def send_otp(request,email):
    totp=pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp=totp.now()
    request.session['otp_secret_key']= totp.secret
    valid_date=datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date']=str(valid_date)
    
    subject = 'verify your email to continue to create an account at Furnics.4U'
    message = otp
    from_email = settings.EMAIL_HOST_USER   
    recipient_list = [ email ] 
    send_mail(subject, message, from_email, recipient_list)  
    print(otp,type(otp))
    return int(otp) 
