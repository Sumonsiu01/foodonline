from django.urls import path

from . import views

urlpatterns = [
    path('registerusers/', views.register, name='registerUser'),
    path('registervendor/', views.register_vendor, name='registerVendor'),
]