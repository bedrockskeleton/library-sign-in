from django import forms
from .models import StudentReference

REASON_CHOICES = [
    ('library', 'Library'),
    ('computer_lab', 'Computer lab'),
    ('esports', 'Esports'),
    ('class', 'Class'),
    ('other', 'Other'),
]

class UnifiedSignInForm(forms.Form):
    student_id = forms.IntegerField(label="Student ID", required=False, min_value=1, max_value=99999)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    reason = forms.ChoiceField(choices=REASON_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get("student_id")
        first_name = cleaned_data.get("first_name", "").strip().title()
        last_name = cleaned_data.get("last_name", "").strip().title()

        # If all three fields are filled out, check if student exists, if not, create them
        if student_id and first_name and last_name:
            qs = StudentReference.objects.filter(student_id=student_id, first_name=first_name, last_name=last_name)
            if not qs.exists():
                StudentReference.objects.create(
                    student_id = student_id,
                    first_name = first_name,
                    last_name = last_name,
                )
        else:
            # Validate that either student_id or (first_name or last_name) is provided
            if not student_id and not (first_name or last_name):
                raise forms.ValidationError("Please provide either a Student ID or at least one of First Name or Last Name.")

            # If student_id is provided, check if it exists
            if student_id:
                if not StudentReference.objects.filter(student_id=student_id).exists():
                    raise forms.ValidationError("No student found with the provided Student ID.")
            else:
                # If only first name is given
                if first_name and not last_name:
                    qs = StudentReference.objects.filter(first_name=first_name)
                    if not qs.exists():
                        raise forms.ValidationError("No student found with the provided first name.")
                    if qs.count() > 1:
                        raise forms.ValidationError("Multiple students found with that first name. Please also specify a last name.")

                # If only last name is given
                elif last_name and not first_name:
                    qs = StudentReference.objects.filter(last_name=last_name)
                    if not qs.exists():
                        raise forms.ValidationError("No student found with the provided last name.")
                    if qs.count() > 1:
                        raise forms.ValidationError("Multiple students found with that last name. Please also specify a first name.")

                # If both first and last name are provided
                elif first_name and last_name:
                    if not StudentReference.objects.filter(first_name=first_name, last_name=last_name).exists():
                        raise forms.ValidationError("No student found with the provided first and last name.")

        return cleaned_data


class ReferenceUploadForm(forms.Form):
    csv_file = forms.FileField()