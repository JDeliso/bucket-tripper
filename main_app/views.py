from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators	import login_required
from .forms import *
from .models import *

# Create your views here.
# splash view
def splash(request):
    return render(request, 'home.html')

# home view
@login_required
def home(request):
    user = request.user
    profile = user.profile
    maps = profile.map_set.all()
    current_map = maps[0]
    context = {'maps': maps, 'current_map': current_map}
    return render(request, 'home.html', context)

# create a new location
@login_required
def create_location(request, map_id):
    current_map = Map.objects.get(id=map_id)

    if request.method == "POST":
        location_form = Location_Form(request.POST)
        print(location_form.errors)

        if location_form.is_valid():
            new_location = location_form.save(commit=False)
            new_location.map_id = current_map

            new_location.save()
        return redirect('home')

# register
def signup(request):
    # if post
    if request.method == "POST":
        # build out data from form
        username_form = request.POST['username']
        email_form = request.POST['email']
        first_name_form = request.POST['first_name']
        last_name_form = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        # validate that passwords match
        if password == password2:
        # check if username exists in db
            if User.objects.filter(username=username_form).exists():
                context = {'error': 'Username is already taken.'}
                return render(request, 'home.html', context)
            else:
                if User.objects.filter(email=email_form).exists():
                    context = {'error':'That email already exists.'}
                    return render(request, 'home.html', context)
                else: 
                # if everything is ok create account
                    user = User.objects.create_user(
                        username=username_form, 
                        email=email_form, 
                        password=password,
                        first_name = first_name_form,
                        last_name = last_name_form)
                    user.save()
                    profile_form = Profile_Form()
                    new_profile = profile_form.save(commit = False)
                    new_profile.user_id = user.id
                    new_profile.save()
                    new_map = Map.objects.create(
                        user_id = user.id
                    )

                    login(request, user)

                    return redirect('/')
        else:
            context = {'error':'Passwords do not match'}
            return render(request, 'home.html', context)
    else:
        # if not post send message, try again 
        context = {'error':'Your account was not created. Please try again.'}
        return redirect(request, '/')