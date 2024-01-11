import time
import pyotp
from django.core.mail import send_mail
# import random
from django.conf import settings
from .models import CustomUser


def get_totp(key):
    totp = pyotp.TOTP(key)
    return totp.now()

def send_otp_mail(email):
    key = pyotp.random_base32()
    subject = 'OTP Verification'
    otp = get_totp(key)
    message = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = CustomUser.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
    
