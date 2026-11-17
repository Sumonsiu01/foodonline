from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages  # ✅ সঠিক ইমপোর্ট
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.form import CategoryForm
from menu.models import Category, FoodItem
from vendor.forms import VendorForm
from vendor.models import Vendor
from accounts.views import check_role_vendor
from django.utils.text import slugify


def get_vendor(request):
    if request.user.is_authenticated:
        try:
            vendor = Vendor.objects.get(user=request.user)
            return vendor
        except Vendor.DoesNotExist:
            return {}
    return {}

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



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    fooditems = FoodItem.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'vendor': vendor,
        'categories': categories,
        'fooditems': fooditems,
    }   
    return render(request, 'vendor/menu_builder.html', context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk, vendor=vendor)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category).order_by('created_at')
    context = {
        'vendor': vendor,
        'category': category,
        'fooditems': fooditems,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)



def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)  # Assign the vendor to the category
            category.slug = slugify(category_name)  # Generate slug from category name
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

def edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)  # Update slug from category name
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)        


def delete_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk, vendor=vendor)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')