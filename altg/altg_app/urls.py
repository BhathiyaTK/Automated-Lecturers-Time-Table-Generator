from django.urls import path
from . import views

urlpatterns = [
    path('', views.userLogin, name='userLogin'),
    path('home/', views.home, name='home'),
    path('home/logout/', views.userLogout, name='userLogout'),
    path('profile/logout/', views.userLogout, name='userLogout'),
    path('register/logout/', views.userLogout, name='userLogout'),
    path('subject/logout/', views.userLogout, name='userLogout'),
    path('hall/logout/', views.userLogout, name='userLogout'),
    path('help/logout/', views.userLogout, name='userLogout'),
    path('profile/', views.profile, name='profile'),
    path('home/table/', views.table, name='table'),
    path('register/', views.register, name='register'),
    path("subject/", views.subject, name="subject"),
    path('hall/', views.hall, name='hall'),
    path('help/', views.help, name='help'),
]