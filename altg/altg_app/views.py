from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect
from .forms import DataForm

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
    form = DataForm()
    context = {'form':form}
    return render(request, 'home.html', context)
    # return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')

def table(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST)
        if data_form.is_valid():
            name = data_form.cleaned_data.get('lecturer_name')
            batch = data_form.cleaned_data['batch']
            hall = data_form.cleaned_data['hall']
            subject = data_form.cleaned_data['subject']
            std_no = data_form.cleaned_data['students']
            data_form.save()
            data_form = DataForm()

            data = {'name': name, 'batch': batch, 'hall': hall, 'subject': subject, 'std_no': std_no}
            return render(request, 'table.html', data)
        else:
            print('********** Not validated **********')
            data_form = DataForm()
            return redirect('home')
        
        print(name, batch, hall, subject, std_no)
    else:
        return render(request, 'home.html')