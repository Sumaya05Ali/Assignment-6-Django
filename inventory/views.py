from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponse
from .forms import PropertyOwnerSignUpForm  

def property_owner_signup(request):
    if request.method == 'POST':
        form = PropertyOwnerSignUpForm(request.POST)
        if form.is_valid():
    
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            
            property_owners_group, created = Group.objects.get_or_create(name='Property Owners')
            property_owners_group.user_set.add(user)

            messages.success(request, 'Your sign-up request has been submitted. Wait for admin approval.')
            return redirect('home')  
    else:
        form = PropertyOwnerSignUpForm()

    return render(request, 'inventory/property_owner_signup.html', {'form': form})

def home_view(request):
    return render(request, 'inventory/home.html')