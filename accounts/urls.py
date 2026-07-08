from django.urls import path

from . import views

urlpatterns = [
    path('registerusers/', views.register, name='registerUser'),
]