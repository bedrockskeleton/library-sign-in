from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required
from .forms import ReferenceUploadForm, StudentReferenceForm
from django.http import HttpResponse
from sign_in.models import StudentReference
import pandas as pd


@admin_required
def upload_reference(request):
    if request.method == 'POST':
        form = ReferenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    return render(request, 'reports/upload_reference.html', {
                        'form': form,
                        'error': "Unsupported file format."
                    })

                df.columns = df.columns.str.strip()  # Always strip whitespace from headers

                # Serialize the DataFrame into JSON and store it in the session
                request.session['uploaded_spreadsheet'] = df.to_json()

                columns = list(df.columns)
                return render(request, 'reports/map_columns.html', {
                    'columns': columns
                })

            except Exception as e:
                return render(request, 'reports/upload_reference.html', {
                    'form': form,
                    'error': f"Error reading file: {e}"
                })
    else:
        form = ReferenceUploadForm()

    return render(request, 'reports/upload_reference.html', {'form': form})



@admin_required
def process_reference_mapping(request):
    if request.method == 'POST':
        id_col = request.POST.get('id_col')
        first_col = request.POST.get('first_col')
        last_col = request.POST.get('last_col')

        spreadsheet_json = request.session.get('uploaded_spreadsheet')
        if not spreadsheet_json:
            return HttpResponse("No spreadsheet found in session", status=400)

        df = pd.read_json(spreadsheet_json)  # Load the DataFrame from JSON

        for _, row in df.iterrows():
            student_id = str(row[id_col]).strip()
            first_name = str(row[first_col]).strip().title()
            last_name = str(row[last_col]).strip().title()

            StudentReference.objects.update_or_create(
                student_id=student_id,
                defaults={'first_name': first_name, 'last_name': last_name}
            )

        # Clear the session after we're done to prevent weirdness
        request.session.pop('uploaded_spreadsheet', None)

        return redirect('reports:upload_success')

    return HttpResponse("Invalid request method", status=405)


@admin_required
def upload_success(request):
    return render(request, 'reports/upload_success.html')


@admin_required
def map_columns(request):
    if request.method == 'POST' and 'spreadsheet' in request.FILES:
        file = request.FILES['spreadsheet']

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except Exception as e:
            return HttpResponse(f"Error reading file: {e}", status=400)

        df.columns = df.columns.str.strip()  # Strip whitespace from headers

        # Store in session (serialized to JSON for persistence)
        request.session['uploaded_df'] = df.to_json()

        return render(request, 'reports/map_columns.html', {
            'columns': df.columns
        })

    return redirect('reports:upload_reference')


@admin_required
def reference_list(request, letter = None):
    if letter:
        references = StudentReference.objects.filter(last_name__istartswith=letter).order_by('last_name', 'first_name')
    else:
        references = StudentReference.objects.all().order_by('last_name', 'first_name')
    return render(request, 'reports/reference_list.html', {'references': references})



@admin_required
def reference_add(request):
    if request.method == 'POST':
        form = StudentReferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reports:reference_list')
    form = StudentReferenceForm()
    return render(request, 'reports/reference_form.html', {'form': form, 'action': 'Add'})

@admin_required
def reference_edit(request, student_id):
    ref = get_object_or_404(StudentReference, student_id=student_id)
    if request.method == 'POST':
        form = StudentReferenceForm(request.POST, instance=ref)
        if form.is_valid():
            form.save()
            return redirect('reports:reference_list')
    else:
        form = StudentReferenceForm(instance=ref)
    return render(request, 'reports/reference_form.html', {'form': form, 'action': 'Edit'})

@admin_required
def reference_delete(request, student_id):
    ref = get_object_or_404(StudentReference, student_id=student_id)
    ref.delete()
    return redirect('reports:reference_list')

@admin_required
def reference_delete_all(request):
    ref = StudentReference.objects.all() # Grabbing all objects
    ref.delete()
    return redirect('reports:reference_list')