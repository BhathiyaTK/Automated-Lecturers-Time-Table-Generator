from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('********* User logged in successfully *********')
            return redirect('home')
        else:
            print('********* Not valid user credentials **********')
            return redirect('/')
    else:
        return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    print('********** User logged out successfully *********')
    return redirect('/')


def home(request):
    return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')