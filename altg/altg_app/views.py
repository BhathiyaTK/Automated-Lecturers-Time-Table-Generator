from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from .forms import DataForm, AddUserForm, AddSubjectForm, AddHallForm
from .models import ProcessData, User, LectureHalls, Subjects, Batch, TimeSlots, Days

# Login function
def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print('***************************** User logged in successfully *********************************')
            return redirect('home')          
        else:
            print('***************************** Not valid user credentials **********************************')
            return redirect('/')
    else:
        return render(request, 'index.html')

# Logout function
def userLogout(request):
    logout(request)
    print('********************************** User logged out successfully **********************************')
    return redirect('/')

# Home page rendering function
def home(request):
    form = DataForm()
    context = {'form':form}
    return render(request, 'home.html', context)

# User add and register page rendering function
def register(request):
    if request.method == 'POST':
        reg_data = AddUserForm(request.POST)
        if reg_data.is_valid():
            first_name = reg_data.cleaned_data.get('first_name')
            last_name = reg_data.cleaned_data.get('last_name')
            lecturer_name = reg_data.cleaned_data.get('lecturer_name')
            lecturer_code = reg_data.cleaned_data.get('lecturer_code')
            email = reg_data.cleaned_data.get('email')
            username = reg_data.cleaned_data.get('username')
            password1 = reg_data.cleaned_data.get('password1')
            password2 = reg_data.cleaned_data.get('password2')
            user_type = reg_data.cleaned_data.get('user_type')

            if password1 == password2:
                if user_type == 'admin':
                    user = User.objects.create_superuser(
                        first_name=first_name,
                        last_name=last_name,
                        lecturer_name=lecturer_name, 
                        lecturer_code=lecturer_code, 
                        username=username, 
                        password=password1, 
                        email=email,
                        is_active=True,
                        is_staff=True
                    )
                    user.save()
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        lecturer_name=lecturer_name, 
                        lecturer_code=lecturer_code, 
                        username=username, 
                        password=password1, 
                        email=email,
                        is_active=True,
                        is_staff=True
                    )
                    user.save()
                    return redirect('register')
            else:
                print('********************** Passwords are not same *************************')
                return redirect('register')
            
        else:
            print('******** User Not Registered ********')
            reg_data = AddUserForm()
            return redirect('register')
    else:
        reg_form = AddUserForm()
        reg_context = {'reg_form':reg_form}
        return render(request, 'register.html', reg_context)

# Lecture hall adding function
def hall(request):
    if request.method == 'POST':
        hall_data = AddHallForm(request.POST)
        if hall_data.is_valid():
            hall_number = hall_data.cleaned_data.get('hall_number')
            hall_name = hall_data.cleaned_data.get('hall_name')

            lec_halls = LectureHalls(hall_number=hall_number, hall_name=hall_name)
            lec_halls.save()
            return redirect('hall')
        else:
            print('********* Lecture Hall Saving Failed **********')
            hall_data = AddHallForm()
            return redirect('hall')
    else:
        hall_form = AddHallForm()
        hall_context = {'hall_form':hall_form}
        return render(request, 'hall.html', hall_context)

# Add subject & subject page rendering function
def subject(request):
    if request.method == 'POST':
        subject_data = AddSubjectForm(request.POST)
        if subject_data.is_valid():
            sub_code = subject_data.cleaned_data.get('subject_code')
            sub_name = subject_data.cleaned_data.get('subject_name')
            rel_batch = subject_data.cleaned_data.get('related_batch')
            
            subjects = Subjects(subject_code=sub_code, subject_name=sub_name, related_batch=rel_batch)
            subjects.save()
            return redirect('subject')
        else:
            print('********** Subject Adding Failed *********')
            subject_data = AddSubjectForm()
            return redirect('subject')
    else:
        subject_form = AddSubjectForm()
        subject_context = {'subject_form':subject_form}
        return render(request, 'subject.html', subject_context)

# Profile page rendering function
def profile(request):
    return render(request, 'profile.html')

# Profile picture updating function
def profileUpdate(request):
    if request.method == 'POST':
        pass

# Help page rendering function
def help(request):
    return render(request, 'help.html')

# Time table generation & visualization
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