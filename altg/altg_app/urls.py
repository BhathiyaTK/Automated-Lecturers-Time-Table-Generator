from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('', views.userLogin, name='userLogin'),
    path('home/', views.home, name='home'),
    path('home/logout/', views.userLogout, name='userLogout'),
    path('profile/logout/', views.userLogout, name='userLogout'),
    path('users/logout/', views.userLogout, name='userLogout'),
    path('subject/logout/', views.userLogout, name='userLogout'),
    path('hall/logout/', views.userLogout, name='userLogout'),
    path('help/logout/', views.userLogout, name='userLogout'),
    path('profile/', views.profile, name='profile'),
    path('home/table/', views.table, name='table'),
    path('users/', views.users, name='users'),
    path("subject/", views.subject, name="subject"),
    path('hall/', views.hall, name='hall'),
    path('help/', views.help, name='help'),
    path('subjectFilter/', views.subjectFilter, name='subjectFilter'),
    path('lecturerFilter/', views.lecturerFilter, name='lecturerFilter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)