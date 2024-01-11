from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

def send_email_client(email):
    subject = "This is a test email"
    message = "This is a test email"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    
    
# def confirmation_email(request, myuser):
#     current_site = get_current_site(request)
#     confirm_subject = "Confirm your email"
#     confirm_msg = render_to_string('email_confirmation.html', {
#         'name':myuser.username,
#         'domain':current_site.domain,
#         'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
#         'token':generate_token.make_token(myuser),
#         })
    
#     email = EmailMessage(
#         confirm_subject,
#         confirm_msg,
#         settings.EMAIL_HOST_USER,
#         [myuser.email],
#     )
#     email.fail_silently = True
#     email.send