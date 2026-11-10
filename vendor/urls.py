from django.contrib import admin
from django.urls import path, include
from . import views

from accounts import views as AccountsViews

urlpatterns = [


 path('',AccountsViews.vendorDashboard, name='vendor'),
 path('profile/', views.vprofile, name='vprofile'),
   
]