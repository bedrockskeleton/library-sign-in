from django.shortcuts import render, redirect
from .models import SignInRecord, StudentReference
from .forms import UnifiedSignInForm, ReferenceUploadForm
from django.utils import timezone
from users.decorators import workstudy_required, admin_required
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from datetime import date
from django.utils.timezone import localtime

import pandas as pd

@workstudy_required
@login_required
def manage_page(request):
    message = None

    if request.method == 'POST':
        form = UnifiedSignInForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            first_name = form.cleaned_data['first_name'].strip().title()
            last_name = form.cleaned_data['last_name'].strip().title()
            reason = form.cleaned_data['reason']

            # Find or create the student reference
            if student_id:
                student_ref, _ = StudentReference.objects.get_or_create(
                    student_id=str(student_id),
                    defaults={'first_name': first_name, 'last_name': last_name}
                )
            else:
                # Search based on available name info
                if first_name and last_name:
                    student_ref = StudentReference.objects.get(first_name=first_name, last_name=last_name)
                elif first_name:
                    student_ref = StudentReference.objects.get(first_name=first_name)
                elif last_name:
                    student_ref = StudentReference.objects.get(last_name=last_name)
                else:
                    # Should never happen because form validation caught it
                    raise ValueError("Missing name information.")

            # Check if student is already signed in
            existing_record = SignInRecord.objects.filter(student=student_ref, time_out__isnull=True).first()
            if existing_record:
                # Sign out the student
                existing_record.time_out = timezone.now()
                existing_record.save()
                message = f"{student_ref.first_name} {student_ref.last_name} signed out."
            else:
                # Sign in the student
                SignInRecord.objects.create(
                    student=student_ref,
                    reason=reason,
                    created_by=request.user
                )
                request.session['last_reason'] = reason  # Store reason in session
                message = f"{student_ref.first_name} {student_ref.last_name} signed in."

            return redirect('sign_in:manage')

    else:
        initial_reason = request.session.get('last_reason', '')
        form = UnifiedSignInForm(initial={'reason': initial_reason})

    today = timezone.localdate()
    current_students = SignInRecord.objects.filter(time_out__isnull=True, time_in__date=today).order_by('-time_in')
    recently_left = SignInRecord.objects.filter(time_out__isnull=False, time_in__date=today).order_by('-time_out')[:10]

    # Apply local time formatting to the current students
    for record in current_students:
        record.local_time_in = localtime(record.time_in).strftime('%I:%M %p').lstrip('0')
        record.local_time_out = localtime(record.time_out).strftime('%I:%M %p').lstrip('0') if record.time_out else '--:-- AM'

    # Apply local time formatting to the recently left students
    for record in recently_left:
        record.local_time_in = localtime(record.time_in).strftime('%I:%M %p').lstrip('0')
        record.local_time_out = localtime(record.time_out).strftime('%I:%M %p').lstrip('0') if record.time_out else '--:-- AM'

    return render(request, 'sign_in/manage_page.html', {
        'form': form,
        'current_students': current_students,
        'recently_left': recently_left,
        'message': message
    })

@login_required
@workstudy_required
def sign_out_student(request, record_id):
    record = SignInRecord.objects.get(id=record_id)
    if not record.time_out:
        record.time_out = timezone.now()
        record.save()
    return redirect('sign_in:manage')

@login_required
def data_page(request):
    records = SignInRecord.objects.select_related('student').order_by('-time_in')
    # Add filtering/sorting logic here
    return render(request, 'sign_in/data_page.html', {'records': records})

import io
from django.http import FileResponse

@login_required
def export_data_excel(request):
    records = SignInRecord.objects.select_related('student').all()
    df = pd.DataFrame([{
        'Student ID': r.student.student_id,
        'Name': f"{r.student.first_name} {r.student.last_name}",
        'Reason': r.reason,
        'Time In': r.time_in,
        'Time Out': r.time_out,
    } for r in records])

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="library_attendance.xlsx")

@login_required
@admin_required
def upload_reference_csv(request):
    if request.method == 'POST':
        form = ReferenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_csv(request.FILES['csv_file'])

            # Normalize column names
            df.columns = df.columns.str.lower().str.strip()

            # Try to infer the correct columns
            id_col = next((col for col in df.columns if 'id' in col), None)
            first_col = next((col for col in df.columns if 'first' in col), None)
            last_col = next((col for col in df.columns if 'last' in col), None)

            if not all([id_col, first_col, last_col]):
                return HttpResponse("Could not find ID, first name, or last name columns", status=400)

            for _, row in df.iterrows():
                StudentReference.objects.update_or_create(
                    student_id=str(row[id_col]).strip(),
                    defaults={
                        'first_name': str(row[first_col]).strip(),
                        'last_name': str(row[last_col]).strip()
                    }
                )
            return redirect('sign_in:reference_list')
    else:
        form = ReferenceUploadForm()

    return render(request, 'sign_in/upload_reference.html', {'form': form})


@login_required
@workstudy_required
def manual_sign_in(request):
    if request.method == 'POST':
        form = ManualSignInForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id'].strip()
            first_name = form.cleaned_data['first_name'].strip()
            last_name = form.cleaned_data['last_name'].strip()
            reason = form.cleaned_data['reason'].strip()

            student_ref, created = StudentReference.objects.get_or_create(
                student_id=student_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name
                }
            )

            SignInRecord.objects.create(
                student=student_ref,
                reason=reason,
                created_by=request.user
            )

            return redirect('sign_in:manage')  # Or wherever you want to go after
    else:
        form = ManualSignInForm()

    return render(request, 'sign_in/manual_sign_in.html', {'form': form})

@login_required
@workstudy_required
def current_students_partial(request):
    today = timezone.localdate()
    records = SignInRecord.objects.filter(
        time_out__isnull=True,
        time_in__date=today
    ).order_by('-time_in')

    for record in records:
        record.local_time_in = localtime(record.time_in).strftime('%I:%M %p').lstrip('0')
        record.local_time_out = localtime(record.time_out).strftime('%I:%M %p').lstrip('0') if record.time_out else '--:-- AM'

    return render(request, 'sign_in/partials/current_students.html', {'current_students': records})

@login_required
@workstudy_required
def recently_left_partial(request):
    today = timezone.localdate()
    records = SignInRecord.objects.filter(
        time_out__isnull=False,
        time_in__date=today
    ).order_by('-time_out')[:10]

    for record in records:
        record.local_time_in = localtime(record.time_in).strftime('%I:%M %p').lstrip('0')
        record.local_time_out = localtime(record.time_out).strftime('%I:%M %p').lstrip('0') if record.time_out else '--:-- AM'

    return render(request, 'sign_in/partials/recently_left.html', {'recently_left': records})

@login_required
@workstudy_required
def undo(request, record_id):
    try:
        record = SignInRecord.objects.get(id=record_id)

        # "Undo" the sign-out
        record.time_out = None
        record.save()

        return redirect('sign_in:manage')
    except SignInRecord.DoesNotExist:
        return HttpResponse("Record not found", status=404)

@login_required
@workstudy_required
def delete_record(request, record_id):
    try:
        record = SignInRecord.objects.get(id=record_id)
        record.delete()
        return redirect('sign_in:manage')
    except SignInRecord.DoesNotExist:
        return HttpResponse("Record not found", status=404)
    
def home(request):
    today = timezone.localdate()
    count = SignInRecord.objects.filter(time_out__isnull=True, time_in__date=today).count()
    context = {
        'count': count,
    }
    return render(request, 'sign_in/home.html', context)