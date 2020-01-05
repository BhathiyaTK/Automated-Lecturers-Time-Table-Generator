from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('home/logout/', views.logout, name='logout'),
    path('profile/logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]