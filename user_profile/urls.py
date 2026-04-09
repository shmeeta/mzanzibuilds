from django.urls import path
from . import views


urlpatterns = [
    path('profile/<str:username>/', views.user_profile, name='profile_page'),
    path('profile-edit/', views.edit_profile, name='edit_profile'),

]