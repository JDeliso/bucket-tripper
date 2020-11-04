from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class User_Form(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')

class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'join_date')

class Map_Form(ModelForm):
    class Meta:
        model = Map
        fields = ('name', 'description')

class Location_Form(ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'description', 'long', 'lat')

class Location_Edit_Form(ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'description')

