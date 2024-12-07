from django.urls import path
from .views import user_form_view,user_list_view

urlpatterns = [
    path('user-form/', user_form_view, name='user_form'),
    path('user-list/',user_list_view,name='user_list'),
]
