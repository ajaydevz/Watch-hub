import pyotp
from datetime import datetime, timedelta


# def send_otp(request):
#     totp=pyotp.TOTP(pyotp.random_base32(),interval=60)
#     otp=pyotp.now()
#     request.session['otp_secret_key']=totp.secret
#     valid_date=datetime.now() + timedelta(minutes=1)
#     request.session['otp_valid_date']=str(valid_date)


#     return otp

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    return otp