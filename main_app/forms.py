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

