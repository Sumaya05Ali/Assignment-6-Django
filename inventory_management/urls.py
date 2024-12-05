# inventory_management/urls.py
from django.contrib import admin
from django.urls import path, include
from inventory.views import home_view  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('inventory/', include('inventory.urls')),  
]
