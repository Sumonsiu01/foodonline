from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path('', views.myAccount, name='myAccount'),
    path('registerusers/', views.register, name='registerUser'),
    path('registervendor/', views.register_vendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('myaccount/', views.myAccount, name='myAccount'),
    path('customerdashboard/', views.customerDashboard, name='customerDashboard'),
    path('vendordashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('vendor/',include('vendor.urls')),
]