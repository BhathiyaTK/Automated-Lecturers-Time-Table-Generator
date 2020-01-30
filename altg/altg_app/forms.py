from django import forms

BATCH = (
    ('', '---- Choose ----'),
    ('1st', '1st Year'),
    ('2nd', '2nd Year'),
    ('3rd', '3rd Year'),
    ('4rd', '4th Year'),
)  
HALL = (
    ('', '---- Choose ----'),
    ('NLH', 'NLH'),
    ('204', '204'),
    ('104', '104'),
    ('Z9', 'Z9'),
)

class DataForm(forms.Form):
    lecturer_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name':'lec_name'}), required=True)
    batch = forms.ChoiceField(choices=BATCH, widget=forms.Select(attrs={'class':'form-control', 'name':'batch'}), required=True)
    hall = forms.ChoiceField(choices=HALL, widget=forms.Select(attrs={'class':'form-control', 'name':'lec_hall'}), required=True)
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name':'subject'}), required=True) 
    students = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name':'std_no'}), required=True)