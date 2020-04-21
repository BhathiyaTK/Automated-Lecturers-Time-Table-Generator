from django import forms
from .models import ProcessData, User, AllLectureHalls, AllSubjects, AllBatches, AllSemesters, Batch, TimeSlots, Days, Profiles

BATCH = (
    ('', '---- Choose ----'),
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
)  
HALL = (
    ('', '---- Choose ----'),
    ('NLH', 'NLH'),
    ('204', '204'),
    ('104', '104'),
    ('Z9', 'Z9'),
)
USER_ROLES = (
    ('', '---- Choose ----'),
    ('admin', 'Admin'),
    ('guest', 'Guest'),
)
TITLES = (
    ('', '---- Choose ----'),
    ('Prof', 'Prof'),
    ('Dr', 'Dr'),
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
)
POSITION = (
    ('', '---- Choose ----'),
    ('lecturer', 'Lecturer'),
    ('demo', 'Demonstrator'),
    ('naStaff', 'Non Acedamic Staff'),
    ('other', 'Other'),
)

class DataForm(forms.Form):
    lecturer_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'lec_name'}), required=True)
    batch = forms.ChoiceField(choices=BATCH, widget=forms.Select(attrs={'class':'form-control form-control-sm', 'name':'batch'}), required=True)
    hall = forms.ChoiceField(choices=HALL, widget=forms.Select(attrs={'class':'form-control form-control-sm', 'name':'lec_hall'}), required=True)
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'subject'}), required=True) 
    students = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'std_no'}), required=True)

class AddUserForm(forms.Form):
    user_title = forms.ChoiceField(choices=TITLES, widget=forms.Select(attrs={'class':'form-control form-control-sm', 'name':'user_title'}), required=True)
    first_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'first_name'}), required=True)
    last_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'last_name'}), required=True)
    lecturer_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'lecturer_name'}), required=True)
    lecturer_code = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'lecturer_code'}), required=True)
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'username'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'name':'password1'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'name':'password2'}), required=True)
    user_type = forms.ChoiceField(choices=USER_ROLES, widget=forms.Select(attrs={'class':'form-control form-control-sm', 'name':'user_type'}), required=True)
    user_position = forms.ChoiceField(choices=POSITION, widget=forms.Select(attrs={'class':'form-control form-control-sm', 'name':'user_position'}), required=True)

class AddHallForm(forms.Form):
    hall_number = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'hall_number'}), required=True)
    hall_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'hall_name'}), required=True)

class DeleteUserForm(forms.Form):
    user_code = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'type':'hidden', 'name':'user_code'}), required=True)

class UserUpdateForm(forms.ModelForm):
    id = forms.CharField(max_length=224, widget=forms.HiddenInput(attrs={'name':'id'}), required=True)
    user_title = forms.ChoiceField(choices=TITLES, widget=forms.Select(attrs={'class':'form-control form-control-sm', 'name':'user_title'}), required=True)
    first_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'first_name'}), required=True)
    last_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'last_name'}), required=True)
    lecturer_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'lecturer_name'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'email'}), required=True)
    lecturer_code = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'lecturer_code'}), required=True)
    username = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'name':'username'}), required=True)

    class Meta:
        model = User
        fields = ['id', 'user_title', 'first_name', 'last_name', 'lecturer_name', 'email', 'lecturer_code', 'username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['user_profile_img']