from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.splash, name="splash"),
    path('home/', views.home, name='home'),
    path('home/<int:map_id>', views.homemap, name='homemap'),
    path('accounts/signup', views.signup, name='signup'),
    path('location/create/<int:map_id>', views.create_location, name='create_location'),
    path('location/delete/<int:location_id>', views.delete_location, name='delete_location'),
    path('maps/create/', views.create_map, name="create_map"),
    path('<str:profile_name>/maps/<int:map_id>', views.view_map, name="view_map"),
    path('location/<int:location_id>/<int:map_id>', views.steal_location, name="steal_location"),
    path('maps/edit/<int:map_id>', views.edit_map, name="edit_map"),
    path('maps/delete/<int:map_id>', views.delete_map, name="delete_map"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)