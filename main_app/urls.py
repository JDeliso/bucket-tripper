from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.splash, name="splash"),
    path('home/', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('location/create/<int:map_id>', views.create_location, name='create_location'),
    path('location/delete/<int:location_id>', views.delete_location, name='delete_location'),
    path('maps/create/', views.create_map, name="create_map"),
    path('<str:profile_name>/maps/<int:map_id>', views.view_map, name="view_map"),
    
]