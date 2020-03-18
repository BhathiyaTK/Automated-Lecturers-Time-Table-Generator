from django import forms

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

class DataForm(forms.Form):
    lecturer_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'name':'lec_name'}), required=True)
    batch = forms.ChoiceField(choices=BATCH, widget=forms.Select(attrs={'class':'form-control', 'name':'batch'}), required=True)
    hall = forms.ChoiceField(choices=HALL, widget=forms.Select(attrs={'class':'form-control', 'name':'lec_hall'}), required=True)
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name':'subject'}), required=True) 
    students = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name':'std_no'}), required=True)

class AddUserForm(forms.Form):
    first_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'first_name'}), required=True)
    last_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'last_name'}), required=True)
    lecturer_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'lecturer_name'}), required=True)
    lecturer_code = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'lecturer_code'}), required=True)
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name':'username'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'name':'password1'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'name':'password2'}), required=True)
    user_type = forms.ChoiceField(choices=USER_ROLES, widget=forms.Select(attrs={'class':'form-control', 'name':'user_type'}), required=True)

class AddSubjectForm(forms.Form):
    subject_code = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'subject_code'}), required=True)
    subject_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'subject_name'}), required=True)
    related_batch = forms.ChoiceField(choices=BATCH, widget=forms.Select(attrs={'class':'form-control', 'name':'related_batch'}), required=True)

class AddHallForm(forms.Form):
    hall_number = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'hall_number'}), required=True)
    hall_name = forms.CharField(max_length=224, widget=forms.TextInput(attrs={'class':'form-control', 'name':'hall_name'}), required=True)