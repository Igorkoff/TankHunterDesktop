from django.urls import path
from .views import *

urlpatterns = [
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', user_register, name='register'),

    path('', world, name='world'),
    path('create_report', create_report, name='create_report'),
    path('update_location/', update_location, name="update_location"),
]