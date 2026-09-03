
from django.shortcuts import render, redirect

from accounts.utils import detectUserRole
from vendor.forms import VendorForm
from .forms import UserForm

from django.contrib import messages
from .models import User, UserProfile

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.decorators import login_required,user_passes_test

from django.core.exceptions import PermissionDenied




#restrict the vendor to access the customer dashboard

def check_role_vendor(user):
    
    if user.role == 1:
        return True
    else:
        raise PermissionDenied('You are not authorized to access this page.')


#restrict the customer to access the vendor dashboard
def check_role_customer(user):
    
    if user.role == 2:
        return True
    else:
        raise PermissionDenied('You are not authorized to access this page.')



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
            user.save()

            messages.success(
                request,
                'Your account has been created successfully. You can now log in.'
            )

            return redirect('login')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

            print("Form is not valid")
            print(form.errors)

    else:

        form = UserForm()

    return render(
        request,
        'accounts/registerUser.html',
        {
            'form': form,
        }
    )


def register_vendor(request):

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')

    if request.method == 'POST':

        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():

            password = form.cleaned_data['password']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )

            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user

            user_profile = UserProfile.objects.get(user=user)

            vendor.user_profile = user_profile
            vendor.save()

            messages.success(
                request,
                'Your account has been created successfully. You can now log in.'
            )

            return redirect('login')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

            print("Form is not valid")
            print(form.errors)
            print(v_form.errors)

    else:

        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(
        request,
        'accounts/registerVendor.html',
        context
    )


def login(request):

    # Already logged-in user should go to dashboard
    if request.user.is_authenticated:
        return redirect('myAccount')

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            messages.success(
                request,
                'You have successfully logged in.'
            )

            return redirect('myAccount')

        else:

            messages.error(
                request,
                'Invalid email or password.'
            )

            return redirect('login')

    return render(
        request,
        'accounts/login.html'
    )


def logout(request):

    auth_logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('login')


def dashboard(request):

    return render(
        request,
        'accounts/dashboard.html'
    )


@login_required(login_url='login')
def myAccount(request):

    user = request.user
    redirectUrl = detectUserRole(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):

    return render(
        request,
        'accounts/customerDashboard.html'
    )

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):

    return render(
        request,
        'accounts/vendorDashboard.html'
    )