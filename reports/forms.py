from django import forms
from sign_in.models import StudentReference
'''
class ReferenceUploadForm(forms.Form):
    file = forms.FileField(label='Upload CSV or Excel file')
    id_column = forms.CharField(label='Student ID Column Name', max_length=100)
    first_name_column = forms.CharField(label='First Name Column Name', max_length=100)
    last_name_column = forms.CharField(label='Last Name Column Name', max_length=100)
'''

class ReferenceUploadForm(forms.Form):
    file = forms.FileField(label="Upload Spreadsheet (.csv or .xlsx)")

class StudentReferenceForm(forms.ModelForm):
    class Meta:
        model = StudentReference
        fields = ['student_id', 'first_name', 'last_name']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }