from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.conf import settings
from .models import *

# Create your views here.
# home view
def home(request):
    return render(request, 'base.html')