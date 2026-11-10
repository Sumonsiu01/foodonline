from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction

from accounts.utils import detectUserRole, send_verification_email, send_password_reset_email
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from vendor.models import Vendor


# Role check functions
def check_role_vendor(user):
    return user.is_authenticated and user.role == User.VENDOR


def check_role_customer(user):
    return user.is_authenticated and user.role == User.CUSTOMER


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.is_active = False  # ইমেইল যাচাই না হওয়া পর্যন্ত অ্যাকাউন্ট নিষ্ক্রিয় থাকবে
            user.save()

            # অ্যাক্টিভেশন ইমেইল পাঠানো
            send_verification_email(request, user)

            messages.success(
                request,
                'Registration successful! Please check your email to activate your account.'
            )
            return redirect('registerUser')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm()

    return render(request, 'accounts/registerUser.html', {'form': form})


def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')

    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # ডাটাবেজ ইন্টিগ্রিটি ঠিক রাখতে ট্রানজাকশন ব্যবহার
            with transaction.atomic():
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                user.role = User.VENDOR
                user.is_active = False
                user.save()

                vendor = v_form.save(commit=False)
                vendor.user = user
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                vendor.user_profile = user_profile
                vendor.save()

                # ভেরিফিকেশন ইমেইল পাঠানো
                send_verification_email(request, user)

            messages.success(
                request,
                'Your vendor account has been registered! Please check your email to activate it.'
            )
            return redirect('registerVendor')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or expired!')
        return redirect('registerUser')


def login(request):
    if request.user.is_authenticated:
        return redirect('myAccount')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirect_url = detectUserRole(user)
    return redirect(redirect_url)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            send_password_reset_email(request, user)
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('forgetPassword')
        else:
            messages.error(request, 'Account does not exist with this email address.')
            return redirect('forgetPassword')

    return render(request, 'accounts/forgetPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired or is invalid.')
        return redirect('forgetPassword')


def resetPassword(request):
    # GET বা POST উভয় ক্ষেত্রে সেশনে uid না থাকলে সরাসরি রিডাইরেক্ট করবে
    uid = request.session.get('uid')
    if not uid:
        messages.error(request, 'Session expired or invalid access. Please try again.')
        return redirect('forgetPassword')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')

        try:
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()

            # নিরাপদ উপায়ে সেশন থেকে uid রিমুভ করা
            request.session.pop('uid', None)

            messages.success(request, 'Password reset successful. You can now log in.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('forgetPassword')

    return render(request, 'accounts/resetPassword.html')