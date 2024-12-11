from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('profile/', views.profile_view, name='profile'),
     path('projects/new/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),
    path('projects/<int:project_id>/phases/new/', views.create_phase, name='create_phase'),
    path('phases/<int:phase_id>/updates/new/', views.create_update, name='create_update'),
    #path('admin/', admin.site.urls, name='admin_dashboard'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
