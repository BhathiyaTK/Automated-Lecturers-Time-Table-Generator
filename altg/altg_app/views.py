from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from .forms import DataForm, AddUserForm, AddHallForm, DeleteUserForm, UserUpdateForm, ProfileUpdateForm
from .models import ProcessData, User, AllLectureHalls, AllSubjects, AllBatches, AllSemesters, AllTimeSlots, Profiles, SavedSchedules
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum, Count
from django.db.models.functions import Cast
from django.db.models import IntegerField
import prettytable as prettytable
import random as rnd
import sys
from subprocess import run, PIPE
from os import popen
import ast
import json

# Login function
def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['logged_username'] = user.username
            login(request, user)
            print('------------- User logged in successfully -------------')
            return redirect('dashboard')          
        else:
            messages.error(request, 'Invalid user login creditials!')
            print('------------- Not valid user credentials -------------')
            return redirect('/')
    else:
        return render(request, 'index.html')

# Logout function
def userLogout(request):
    logout(request)
    print('------------- User logged out successfully -------------')
    return redirect('/')

# Dashboard page functions
def dashboard(request):
    profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
    lecturers_count = User.objects.filter(user_position='lecturer').count()
    others_count = User.objects.exclude(user_position='lecturer').count()
    subjects_count = AllSubjects.objects.count()
    students_count = AllBatches.objects.all().annotate(as_int=Cast('no_of_students', IntegerField())).aggregate(Sum('as_int'))
    all_users = User.objects.all().order_by('id')
    dashboard_context = {
        'profile_photo':profile_photo,
        'all_users':all_users,
        'lecturers_count':lecturers_count,
        'others_count':others_count,
        'subjects_count':subjects_count,
        'students_count':students_count,
    }
    return render(request, 'dashboard.html', dashboard_context)

# Dashboard chart function
def dashChart(request):
    if request.method == 'GET':
        labels = []
        data_values = []

        dataset = AllSubjects.objects.exclude(related_lecturer='Not assigned').values('related_lecturer').annotate(data_count = Count('related_lecturer')).order_by('-data_count')
        for sub in dataset:
            labels.append(sub['related_lecturer'])
            data_values.append(sub['data_count'])
        data = {
            "labels": labels,
            "data_values": data_values,
        }
        return JsonResponse(data)
    else:
        return redirect('dashboard')

# Schedule page function
def schedule(request):
    if request.method == 'POST':
        lec_name = request.POST['selected_lecturer']
        sem = request.POST['selected_semester']
        if (lec_name and sem) is not None:
            out = run([sys.executable,'D://Web Projects//CIS_ALTG//altg//gAlgorithm.py',lec_name, sem],shell=False,stdout=PIPE)
            byteVal = (out.stdout).strip()
            strVal = byteVal.decode()
            data_list = ast.literal_eval(strVal)
            # data_list_str = str(data_list).strip('[]')
            # print(type(data_list_str))
            data_table_row = []
            hall_n_time = []
            for i in data_list:
                data_table_row.append("<tr><td>"+i[0]+"</td><td>"+i[1]+"</td><td>"+i[2]+"</td><td>"+i[3]+"</td></tr>")
                hall_n_time.append(i[2]+","+i[3])
            lecturer_names = User.objects.filter(user_position='lecturer')
            semester_info = AllSemesters.objects.all()
            profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
            context = {
                'lecturer_names': lecturer_names, 
                'profile_photo': profile_photo,
                'schedule_data': data_table_row,
                'hall_n_time': hall_n_time,
                'data_str': data_list,
                'lec_name': lec_name,
                'semester': sem,
                'semester_info': semester_info
                }
            return render(request, 'schedule.html', context)
        else:
            messages.error(request, 'Please select both fields!')
            lecturer_names = User.objects.filter(user_position='lecturer')
            semester_info = AllSemesters.objects.all()
            profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
            context = {'lecturer_names': lecturer_names,'profile_photo': profile_photo, 'semester_info': semester_info}
            return render(request, 'schedule.html', context)
    else:
        lecturer_names = User.objects.filter(user_position='lecturer')
        semester_info = AllSemesters.objects.all()
        profile_photo = Profiles.objects.filter(
            username=request.session['logged_username'])
        context = {'lecturer_names': lecturer_names,'profile_photo': profile_photo,'semester_info': semester_info}
        return render(request, 'schedule.html', context)

# Schedule save function
def scheduleSave(request):
    # pass
    if request.method == 'GET':
        lec_name = request.GET['lecturer_name']
        sem = request.GET['semester']
        hall_time = request.GET['hall_n_time']
        lec_schedule = request.GET['data_str']
        if (lec_name and sem and hall_time and lec_schedule) is not None:
            schedule = SavedSchedules(lecturer_name=lec_name, semester=sem, hall_n_time=hall_time, schedule=lec_schedule)
            schedule.save()

            print('Saving successfull')
            return JsonResponse({'success': 'Lecture Schedule Saved Successfully.'})
        else:
            print('Saving failed')
            return JsonResponse({'error': 'Schedule Saving Failed.'})
    else:
        print('Saving failed')
        return redirect('schedule')

# Lecture hall page function
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
    elif 'hall_edit_btn' in request.POST:
        if request.method == 'POST':
            hall_code = request.POST['hall_code']
            new_hall_number = request.POST['new_hall_number']
            new_hall_name = request.POST['new_hall_name']
            AllLectureHalls.objects.filter(Q(id=hall_code)).update(
                hall_number=new_hall_number,
                hall_name=new_hall_name
            )
            messages.success(request, 'Hall updated successfully!')
            return redirect('hall')
    elif 'batch_edit_btn' in request.POST:
        if request.method == 'POST':
            batch_code = request.POST['batch_code']
            new_no_of_students = request.POST['new_no_of_students']
            AllBatches.objects.filter(Q(id=batch_code)).update(
                no_of_students = request.POST['new_no_of_students']
            )
            messages.success(request, 'Batch data updated successfully!')
            return redirect('hall')
    else:
        halls_data = AllLectureHalls.objects.all()
        batch_data = AllBatches.objects.all()
        hall_form = AddHallForm()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        hall_context = {'hall_form':hall_form, 'halls_data':halls_data, 'profile_photo':profile_photo, 'batch_data':batch_data}
        return render(request, 'hall.html', hall_context)

# Lecturer-wise subject filter function
def lecturerFilter(request):
    if request.method == 'GET':
        lecturerVal = request.GET['lecturerVal']
        if lecturerVal == 'all':
            filtered_data = AllSubjects.objects.all().order_by('related_batch','semester')
            data = serializers.serialize('json', filtered_data)
        else:
            filtered_data = AllSubjects.objects.filter(Q(related_lecturer=lecturerVal)).order_by('related_batch','semester')
            data = serializers.serialize('json', filtered_data)
        print('Filtering successfull')
        return HttpResponse(data, content_type="text/json-comment-filtered")
    else:
        print('Filtering failed')
        return redirect('subject')

# Batch-wise subject filter function
def subjectFilter(request):
    if request.method == 'GET':
        filterVal = request.GET['filterVal']
        if filterVal == 'all':
            filtered_data = AllSubjects.objects.all().order_by('related_batch','semester')
            data = serializers.serialize('json', filtered_data)
        else:
            filtered_data = AllSubjects.objects.filter(Q(related_batch=filterVal)).order_by('related_batch','semester')
            data = serializers.serialize('json', filtered_data)
        print('Filtering successfull')
        return HttpResponse(data, content_type="text/json-comment-filtered")
    else:
        print('Filtering failed')
        return redirect('subject')

# Subjects manage & subject page function
def subject(request):
    if 'subject_add_btn' in request.POST:
        if request.method == 'POST':
            sub_code = request.POST['subject_code']
            sub_name = request.POST['subject_name']
            rel_batch = request.POST['related_batch']
            semester = request.POST['semester']
            rel_lecturer = request.POST['related_lecturer']

            if (sub_code and sub_name and rel_batch and rel_lecturer and semester) is not None:            
                subjects = AllSubjects(subject_code=sub_code, subject_name=sub_name, related_batch=rel_batch, related_lecturer=rel_lecturer, semester=semester)
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

    elif 'subject_delete_btn' in request.GET:
        if request.method == 'GET':
            subject_code = request.GET['subject_code']
            AllSubjects.objects.filter(Q(subject_code=subject_code)).delete()
            messages.success(request, 'Subject deleted successfully')
            return redirect('subject')
        else:
            print('------------- Subject deletion failed -------------')
            message.error(request, 'Subject deletion failed! Try again later.')
            return redirect('subject')
    elif 'subject_edit_btn' in request.POST:
        if request.method == 'POST':
            new_subject_code = request.POST['new_subject_code']
            new_subject_name = request.POST['new_subject_name']
            new_related_lecturer = request.POST['new_related_lecturer']
            new_batch = request.POST['new_batch']
            new_semester = request.POST['new_semester']
            subject_code = request.POST['subject_code']
            AllSubjects.objects.filter(Q(id=subject_code)).update(
                subject_code=new_subject_code,
                subject_name=new_subject_name,
                related_lecturer=new_related_lecturer,
                related_batch=new_batch,
                semester=new_semester
            )
            messages.success(request, 'Subject updated successfully!')
            return redirect('subject')
        else:
            print('------------- Subject deletion failed -------------')
            messages.error(request, 'Subject deletion failed! Try again later.')
            return redirect('subject')
    else:
        lecturers_data = User.objects.all()
        subjects_data = AllSubjects.objects.all().order_by('related_batch','semester')
        batch_data = AllBatches.objects.all().order_by('batch_no')
        semester_data = AllSemesters.objects.all()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        subject_context = {
            'lecturers_data':lecturers_data,
            'subjects_data':subjects_data,
            'profile_photo':profile_photo,
            'batch_data':batch_data,
            'semester_data':semester_data
        }
        return render(request, 'subject.html', subject_context)

# Users manage and user page function
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
                user_position = reg_data.cleaned_data.get('user_position')
                default_profile_img = 'users/profile.jpg'

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
                            user_position=user_position
                        )
                        prof_img = Profiles(username=username, user_profile_img=default_profile_img)
                        user.save()
                        prof_img.save()
                        messages.success(request, 'User has been registered successfully!')
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
                            user_position=user_position
                        )
                        prof_img = Profiles(username=username, user_profile_img=default_profile_img)
                        user.save()
                        prof_img.save()
                        messages.success(request, 'User has been registered successfully!')
                        return redirect('users')
                else:
                    print('********************** Passwords are not same *************************')
                    messages.warning(request, 'Passwords are not match each other!')
                    return redirect('users')    
            else:
                print('******** User Not Registered ********')
                messages.error(request, 'User registration failed!')
                reg_data = AddUserForm()
                return redirect('users')
        else:
            lecturers_values = User.objects.all()
            myDate = datetime.now()
            formatedDate = myDate.strftime("%d-%m-%Y")
            reg_form = AddUserForm()
            user_delete_form = DeleteUserForm()
            profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
            reg_context = {'reg_form':reg_form, 'user_delete_form':user_delete_form, 'lecturers_values':lecturers_values, 'profile_photo':profile_photo, 'date':formatedDate}
            return render(request, 'users.html', reg_context)

    elif 'user_delete_btn' in request.POST:
        if request.method == 'POST':
            user_code = request.POST['user_code']
            User.objects.filter(Q(id=user_code)).delete()
            messages.success(request, 'User deleted successfully!')
            print(user_code)
            return redirect('users')
        else:
            print('------------------ Lecturer deletion failed -----------------')
            messages.error(request, 'User deletion failed! Try again later.')
            return redirect('users')
    else:
        lecturers_values = User.objects.all()
        myDate = datetime.now()
        formatedDate = myDate.strftime("%d-%m-%Y")
        reg_form = AddUserForm()
        user_delete_form = DeleteUserForm()
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
        reg_context = {'reg_form':reg_form, 'user_delete_form':user_delete_form, 'lecturers_values':lecturers_values, 'profile_photo':profile_photo, 'date':formatedDate}
        return render(request, 'users.html', reg_context)

# Profile page function
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm()
        if user_update_form.is_valid() or profile_update_form.is_valid():
            profile_image = request.FILES.get('user_profile_img')
            new_user_title = request.POST['user_title']
            profile_id = request.POST['id']
            new_first_name = request.POST['first_name']
            new_last_name = request.POST['last_name']
            new_lecturer_name = request.POST['lecturer_name']
            new_email = request.POST['email']
            new_lecturer_code = request.POST['lecturer_code']
            new_username = request.POST['username']

            if profile_image is None:
                User.objects.filter(Q(id=profile_id)).update(
                    user_title=new_user_title,
                    first_name=new_first_name,
                    last_name=new_last_name,
                    lecturer_name=new_lecturer_name,
                    email=new_email,
                    lecturer_code=new_lecturer_code,
                    username=new_username
                )
                exist_profile = Profiles.objects.filter(username=request.session['logged_username'])
                exist_profile_path = Profiles.objects.get(username=request.session['logged_username'])
                if exist_profile is not None:
                    Profiles.objects.filter(username=request.session['logged_username']).delete()
                    updated_profile_img = Profiles(username=request.session['logged_username'], user_profile_img=exist_profile_path.user_profile_img)
                    updated_profile_img.save()
                    messages.success(request, 'Your profile updated successfully!')
                    return redirect('profile')
                else:
                    updated_profile_img = Profiles(username=request.session['logged_username'], user_profile_img=exist_profile_path.user_profile_img)
                    updated_profile_img.save()
                    messages.success(request, 'Your profile updated successfully!')
                    return redirect('profile')
                messages.success(request, 'Your profile updated successfully!')
                return redirect('profile')
            else:
                User.objects.filter(Q(id=profile_id)).update(
                    user_title=new_user_title,
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
                    messages.success(request, 'Your profile updated successfully!')
                    return redirect('profile')
                else:
                    updated_profile_img = Profiles(username=request.session['logged_username'], user_profile_img=profile_image)
                    updated_profile_img.save()
                    messages.success(request, 'Your profile updated successfully!')
                    return redirect('profile')
        else:
            messages.error(request, 'Profile updating process failed! Something went wrong. Try again.')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=Profiles)
        profile_photo = Profiles.objects.filter(username=request.session['logged_username'])

        profile_values = User.objects.filter(username=request.session['logged_username'])
        p = profile_values.values('lecturer_name')
        for lec in p:
            lecturers_subjects = AllSubjects.objects.filter(related_lecturer=lec['lecturer_name'])

        lec_name = str(list(profile_values.values_list('lecturer_name', flat=True))).strip("['']")
        schedule_data = SavedSchedules.objects.filter(lecturer_name=lec_name).values_list('schedule', flat=True)
        s_data_list = str(list(schedule_data)).strip('[]')
        convert_list = ast.literal_eval(json.loads(s_data_list))
        s_data_table_row = []
        for i in convert_list:
            s_data_table_row.append("<tr><td>"+i[0]+"</td><td>"+i[1]+"</td><td>"+i[2]+"</td><td>"+i[3]+"</td></tr>")
        
        profile_context = {
            'profile_values':profile_values,
            'profile_photo':profile_photo,
            'user_update_form':user_update_form,
            'lecturers_subjects':lecturers_subjects,
            'profile_update_form':profile_update_form,
            'schedule_info':s_data_table_row
        }
        return render(request, 'profile.html', profile_context)

# Help page  function
def settings(request):
    profile_photo = Profiles.objects.filter(username=request.session['logged_username'])
    help_context = {'profile_photo':profile_photo}
    return render(request, 'settings.html', help_context)
