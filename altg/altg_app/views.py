from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from .forms import DataForm, AddUserForm, AddHallForm, DeleteUserForm, UserUpdateForm, ProfileUpdateForm
from .models import ProcessData, User, AllLectureHalls, AllSubjects, Batch, TimeSlots, Days, Profiles
from django.contrib import messages
from django.db.models import Q

# Login function
def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['logged_username'] = username
            login(request, user)
            print('------------- User logged in successfully -------------')
            return redirect('home')          
        else:
            print('------------- Not valid user credentials -------------')
            return redirect('/')
    else:
        return render(request, 'index.html')

# Logout function
def userLogout(request):
    logout(request)
    print('------------- User logged out successfully -------------')
    return redirect('/')

# Home page rendering function
def home(request):
    lecturer_names = User.objects.all()
    form = DataForm()
    profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
    context = {'form':form, 'lecturer_names': lecturer_names, 'profile_photo':profile_photo}
    return render(request, 'home.html', context)

# Lecture hall adding function
def hall(request):
    if 'hall_add_btn' in request.POST:
        if request.method == 'POST':
            hall_data = AddHallForm(request.POST)
            if hall_data.is_valid():
                hall_number = hall_data.cleaned_data.get('hall_number')
                hall_name = hall_data.cleaned_data.get('hall_name')

                lec_halls = AllLectureHalls(hall_number=hall_number, hall_name=hall_name)
                lec_halls.save()
                messages.success(request, 'Lecture hall added successfully!')
                return redirect('hall')
            else:
                print('********* Lecture Hall Adding Failed **********')
                messages.error(request, 'Lecture hall adding failed! Try again later.')
                hall_data = AddHallForm()
                return redirect('hall')
        else:
            halls_data = AllLectureHalls.objects.all()
            hall_form = AddHallForm()
            profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
            hall_context = {'hall_form':hall_form, 'halls_data':halls_data, 'profile_photo':profile_photo}
            return render(request, 'hall.html', hall_context)

    elif 'hall_delete_btn' in request.POST:
        if request.method == 'POST':
            hall_code = request.POST['hall_code']
            AllLectureHalls.objects.filter(Q(id=hall_code)).delete()
            messages.success(request, 'Lecture hall deleted successfully!')
            return redirect('hall')
        else:
            print('------------- Lecture hall deletion failed -------------')
            messages.error(request, 'Lecture hall deletion failed! Try again later.')
            return redirect('hall')
    else:
        halls_data = AllLectureHalls.objects.all()
        hall_form = AddHallForm()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        hall_context = {'hall_form':hall_form, 'halls_data':halls_data, 'profile_photo':profile_photo}
        return render(request, 'hall.html', hall_context)

# Subjects manage & subject page rendering function
def subject(request):
    if 'subject_add_btn' in request.POST:
        if request.method == 'POST':
            sub_code = request.POST['subject_code']
            sub_name = request.POST['subject_name']
            rel_batch = request.POST['related_batch']
            rel_lecturer = request.POST['related_lecturer']

            if (sub_code and sub_name and rel_batch and rel_lecturer) is not None:            
                subjects = AllSubjects(subject_code=sub_code, subject_name=sub_name, related_batch=rel_batch, related_lecturer=rel_lecturer)
                subjects.save()
                messages.success(request, 'Subject added successfully!')
                return redirect('subject')
            else:
                print('------------ Subject adding failed ------------')
                messages.error(request, 'Subject adding failed! Try again.')
                subject_data = AddSubjectForm()
                return redirect('subject')
        else:
            lecturers_data = User.objects.all()
            subjects_data = AllSubjects.objects.all()
            subject_form = AddSubjectForm()
            profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
            subject_context = {'subject_form':subject_form, 'lecturers_data':lecturers_data, 'subjects_data':subjects_data, 'profile_photo':profile_photo}
            return render(request, 'subject.html', subject_context)

    elif 'subject_delete_btn' in request.POST:
        if request.method == 'POST':
            subject_code = request.POST['subject_code']
            AllSubjects.objects.filter(Q(id=subject_code)).delete()
            messages.success(request, 'Subject deleted successfully')
            return redirect('subject')
        else:
            print('------------- Subject deletion failed -------------')
            message.error(request, 'Subject deletion failed! Try again later.')
            return redirect('subject')
    else:
        lecturers_data = User.objects.all()
        subjects_data = AllSubjects.objects.all()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        subject_context = {'lecturers_data':lecturers_data, 'subjects_data':subjects_data, 'profile_photo':profile_photo}
        return render(request, 'subject.html', subject_context)

# Users manage and user page rendering function
def users(request):
    if 'user_add_btn' in request.POST:
        if request.method == 'POST':
            reg_data = AddUserForm(request.POST)
            if reg_data.is_valid():
                user_title = reg_data.cleaned_data.get('user_title')
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
                            user_title=user_title,
                            first_name=first_name,
                            last_name=last_name,
                            lecturer_name=lecturer_name, 
                            lecturer_code=lecturer_code, 
                            username=username, 
                            password=password1, 
                            email=email,
                            is_active=True,
                            is_staff=True,
                            user_profile='profile.jpg'
                        )
                        user.save()
                        messages.success(request, 'Lecturer was added successfully!')
                        return redirect('users')
                    else:
                        user = User.objects.create_user(
                            user_title=user_title,
                            first_name=first_name,
                            last_name=last_name,
                            lecturer_name=lecturer_name, 
                            lecturer_code=lecturer_code, 
                            username=username, 
                            password=password1, 
                            email=email,
                            is_active=True,
                            is_staff=True,
                            user_profile='profile.jpg'
                        )
                        user.save()
                        messages.success(request, 'Lecturer was registered successfully!')
                        return redirect('users')
                else:
                    print('********************** Passwords are not same *************************')
                    messages.warning(request, 'Passwords are not match each other!')
                    return redirect('users')    
            else:
                print('******** User Not Registered ********')
                messages.error(request, 'Lecturer registration failed!')
                reg_data = AddUserForm()
                return redirect('users')
        else:
            lecturers_values = User.objects.all()
            reg_form = AddUserForm()
            user_delete_form = DeleteUserForm()
            profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
            reg_context = {'reg_form':reg_form, 'user_delete_form':user_delete_form, 'lecturers_values':lecturers_values, 'profile_photo':profile_photo}
            return render(request, 'users.html', reg_context)

    elif 'user_delete_btn' in request.POST:
        if request.method == 'POST':
            user_code = request.POST['user_code']
            User.objects.filter(Q(id=user_code)).delete()
            messages.success(request, 'Lecturer deleted successfully!')
            print(user_code)
            return redirect('users')
        else:
            print('------------------ Lecturer deletion failed -----------------')
            messages.error(request, 'Lecturer deletion failed! Try again later.')
            return redirect('users')
    else:
        lecturers_values = User.objects.all()
        reg_form = AddUserForm()
        user_delete_form = DeleteUserForm()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        reg_context = {'reg_form':reg_form, 'user_delete_form':user_delete_form, 'lecturers_values':lecturers_values, 'profile_photo':profile_photo}
        return render(request, 'users.html', reg_context)

# Profile page rendering function
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            profile_image = request.FILES['user_profile_img']
            profile_id = request.POST['id']
            new_first_name = request.POST['first_name']
            new_last_name = request.POST['last_name']
            new_lecturer_name = request.POST['lecturer_name']
            new_email = request.POST['email']
            new_lecturer_code = request.POST['lecturer_code']
            new_username = request.POST['username']

            User.objects.filter(Q(id=profile_id)).update(
                first_name=new_first_name,
                last_name=new_last_name,
                lecturer_name=new_lecturer_name,
                email=new_email,
                lecturer_code=new_lecturer_code,
                username=new_username
            )
            exist_profile = Profiles.objects.filter(username=request.session['logged_username'])
            if exist_profile is not None:
                Profiles.objects.filter(username=request.session['logged_username']).delete()
                updated_profile_img = Profiles(username=request.session['logged_username'], user_profile_img=profile_image)
                updated_profile_img.save()
                messages.success(request, 'User details updated successfully!')
                return redirect('profile')
            else:
                updated_profile_img = Profiles(username=request.session['logged_username'], user_profile_img=profile_image)
                updated_profile_img.save()
                messages.success(request, 'User details updated successfully!')
                return redirect('profile')
            
        else:
            messages.error(request, 'User details updating failed! Try again.')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=Profiles)
        profile_values = User.objects.all()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        profile_context = {
            'profile_values':profile_values,
            'profile_photo':profile_photo,
            'user_update_form':user_update_form,
            'profile_update_form':profile_update_form
        }
        return render(request, 'profile.html', profile_context)

# Help page rendering function
def help(request):
    profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
    help_context = {'profile_photo':profile_photo}
    return render(request, 'help.html', help_context)

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