from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('home/', views.home, name="home"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path("logout/", views.logOut, name ="logout"), 
    path("create-project/", views.create_project, name ="create_post"), 
    path('project/<int:pk>/update', views.update_project, name="update_project"), 
    path('celebration-wall/', views.celebration_wall, name='celebration_wall'), 
    path('send-collab-request/<int:project_id>/', views.send_collaboration_request, name='send_collab_request' ),
    path('celebrate-project/<int:project_id>/', views.send_celebration_notification, name='send_celebration'),
    path('notifications/',views.notifications_view, name="notifications"),
    path('view-project/<int:pk>/', views.project_details, name='project_details')
]