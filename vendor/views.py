from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages  # ✅ সঠিক ইমপোর্ট
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from vendor.forms import VendorForm
from vendor.models import Vendor
from accounts.views import check_role_vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('vprofile')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'vendor': vendor,
        'profile': profile,
    }
    return render(request, 'vendor/vprofile.html', context)