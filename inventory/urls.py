# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.property_owner_signup, name='property_owner_signup'),
]
