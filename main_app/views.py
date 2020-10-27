from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from django.contrib.auth.decorators	import login_required

# Create your views here.
# home view
def home(request):
    return render(request, 'home.html')

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

                    login(request, user)

                    return redirect('/')
        else:
            context = {'error':'Passwords do not match'}
            return render(request, 'home.html', context)
    else:
        # if not post send message, try again 
        context = {'error':'Your account was not created. Please try again.'}
        return redirect(request, '/')