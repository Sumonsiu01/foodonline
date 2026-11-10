from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def detectUserRole(user):
    if user.role == 1:
        return 'vendorDashboard'
    elif user.role == 2:
        return 'customerDashboard'
    elif user.role is None and user.is_superadmin:
        return '/admin'
    return 'login'


def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    
    # Domain safe retrieval (request thakle host nibe, na hole fallback domain)
    if request is not None:
        current_site = get_current_site(request)
        domain = current_site.domain
    else:
        domain = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')

    mail_subject = 'Activate your account'
    
    context = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    message = render_to_string('accounts/emails/account_verification_email.html', context)
    to_email = user.email
    
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


def send_password_reset_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL

    if request is not None:
        current_site = get_current_site(request)
        domain = current_site.domain
    else:
        domain = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')

    mail_subject = 'Reset Your Password'
    
    context = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    message = render_to_string('accounts/emails/reset_password_email.html', context)
    to_email = user.email

    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()


def send_notification_email(mail_subject, mail_template, context):
    """
    Vendor approval ba onnanno generic system notifications pathanor helper function.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context.get('to_email')
    
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = 'html'
    mail.send()