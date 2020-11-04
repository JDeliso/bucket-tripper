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
    locations = current_map.location_set.all()
    context = {'maps': maps, 'current_map': current_map, 'profile': profile, 'locations': locations}
    return render(request, 'home.html', context)

@login_required
def homemap(request, map_id):
    user = request.user
    profile = user.profile
    maps = profile.map_set.all()
    current_map = Map.objects.get(id=map_id)
    locations = current_map.location_set.all()
    context = {'maps': maps, 'current_map': current_map, 'profile': profile, 'locations': locations}
    return render(request, 'home.html', context)

@login_required
def view_map(request, map_id, profile_name):
    profile = User.objects.get(username=profile_name)
    profile = Profile.objects.get(user_id=profile.id)
    current_map = Map.objects.get(id=map_id)
    profile_maps = profile.map_set.all()
    locations = current_map.location_set.all()
    your_maps = request.user.profile.map_set.all()
    context = {'maps': profile_maps, 'current_map': current_map, 'profile': profile, 'locations': locations, 'yourmaps': your_maps}
    return render(request, 'view.html', context)

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
        return redirect('homemap', current_map.id)

def edit_location(request, location_id):
    location = Location.objects.get(id=location_id)

    if request.method == "POST":
        edit_location_form = Location_Edit_Form(request.POST, instance=location)
        if edit_location_form.is_valid():
            location = edit_location_form.save()
            location.save()
        
        return redirect("homemap", location.map_id.id)

@login_required
def delete_location(request, location_id):
    doomed_location = Location.objects.get(id=location_id)

    if request.user.id == doomed_location.map_id.user_id:
        current_map = doomed_location.map_id
        doomed_location.delete()
    else:
        return redirect('home')
    return redirect('homemap', current_map.id)

@login_required
def create_map(request):
    if request.method == "POST":

        map_form = Map_Form(request.POST)
        print(map_form.errors)

        if map_form.is_valid():
            new_map = map_form.save(commit=False)
            new_map.user_id = request.user.id

        new_map.save()

        return redirect('home')

@login_required
def edit_map(request, map_id):
    map = Map.objects.get(id=map_id)

    if request.method == 'POST':
        map_form = Map_Form(request.POST, instance=map)
        if map_form.is_valid():
            if request.user.username == map.user.user.username:
                map = map_form.save()
                map.save()
        return redirect('homemap', map_id)

@login_required
def delete_map(request, map_id):
    doomed_map = Map.objects.get(id=map_id)

    if request.user.username == doomed_map.user.user.username:
        if request.POST['delete_text'] == 'delete':
            doomed_map.delete()

    return redirect('home')
        



@login_required
def steal_location(request, location_id, map_id):
    location = Location.objects.get(id=location_id)
    new_map = Map.objects.get(id=map_id)
    new_location = Location.objects.create(
        name = location.name,
        description = location.description,
        long = location.long,
        lat = location.lat,
        map_id = new_map,
    )
    new_location.save()

    print(location.map_id.id)
    print(location.map_id.user.user.username)
    return redirect('view_map', location.map_id.user.user.username, location.map_id.id)
    

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