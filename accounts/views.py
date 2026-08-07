from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm

from django.contrib import messages

from .models import User, UserProfile

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']

            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()

            messages.success(request, 'Your account has been created successfully. You can now log in.')

            return redirect('registerUser')
        else:
            messages.error(request, 'Please correct the errors below.')
            print("Form is not valid")
            print(form.errors)

    else:
        form = UserForm()

    return render(request, 'accounts/registerUser.html', {
        'form': form,
    })



def register_vendor(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

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

            return redirect('registerVendor')

        else:
            messages.error(request, 'Please correct the errors below.')

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