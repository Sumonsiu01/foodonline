from django.urls import path

from . import views

urlpatterns = [
    path('registerusers/', views.register, name='registerUser'),
    path('registervendor/', views.register_vendor, name='registerVendor'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myAccount, name='myAccount'),
    path('customerdashboard/', views.customerDashboard, name='customerDashboard'),
    path('vendordashboard/', views.vendorDashboard, name='vendorDashboard'),
]