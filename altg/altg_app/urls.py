from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('', views.userLogin, name='userLogin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule/', views.schedule, name='schedule'),
    path('logout/', views.userLogout, name='userLogout'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users'),
    path("subject/", views.subject, name="subject"),
    path('hall/', views.hall, name='hall'),
    path('help/', views.help, name='help'),
    path('subjectFilter/', views.subjectFilter, name='subjectFilter'),
    path('lecturerFilter/', views.lecturerFilter, name='lecturerFilter'),
    path('dashChart/', views.dashChart, name='dashChart'),
    path('scheduleSave/', views.scheduleSave, name='scheduleSave'),
    path('reset/', views.reset, name='reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
