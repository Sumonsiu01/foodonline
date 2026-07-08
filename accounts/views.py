from django.shortcuts import render, redirect
from .forms import UserForm

from django.contrib import messages

from .models import User

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