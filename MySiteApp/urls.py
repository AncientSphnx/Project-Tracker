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
    path('progress-tracker/', views.progress_tracker, name='progress_tracker'),
    path('projects/new/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('projects/', views.all_projects, name='all_projects'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'), 
    path('phases/<int:phase_id>/details/', views.phase_details, name='phase_details'),
    path('projects/<int:project_id>/phases/new/', views.create_phase, name='create_phase'),
    path('phases/<int:phase_id>/updates/', views.create_update, name='create_update'),
    path('phases/<int:phase_id>/delete/', views.delete_phase, name='delete_phase'),
    #path('admin/', admin.site.urls, name='admin_dashboard'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('allocated/', views.allocated_students_view, name='allocated_students'),
    path('mentor/projects/', views.mentor_student_projects, name='mentor_student_projects'),
    path('projects/<int:project_id>/mentor/', views.project_detail_mentor, name='project_detail_mentor'),
     path('resource/delete/<int:resource_id>/', views.delete_resource, name='delete_resource'),
]
