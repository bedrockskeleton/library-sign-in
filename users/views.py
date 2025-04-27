from django.contrib.auth import login, logout, authenticate
from users.decorators import workstudy_required, admin_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomAuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from users.forms import WorkstudyForm

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.default_password_used:
                return redirect('users:force_password_change')
            return redirect('sign_in:manage')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('sign_in:home')


def force_password_change(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            request.user.set_password(password1)
            request.user.default_password_used = False
            request.user.save()
            login(request, request.user)  # Re-login after password change
            return redirect('sign_in:manage')
        else:
            return render(request, 'users/force_password_change.html', {'error': 'Passwords do not match.'})
    return render(request, 'users/force_password_change.html')



User = get_user_model()

@admin_required
def workstudy_list(request):
    workstudies = User.objects.filter(is_workstudy=True, is_superuser = False)
    admins = User.objects.filter(is_superuser = True)
    return render(request, 'users/workstudy_list.html', {
        'workstudies': workstudies,
        'admins': admins
        })

@admin_required
def workstudy_add(request):
    if request.method == 'POST':
        form = WorkstudyForm(request.POST)
        if form.is_valid():
            workstudy = form.save(commit=False)
            workstudy.is_workstudy = True
            workstudy.set_password('0akl@ndL1br@ry2025')
            workstudy.must_change_password = True
            workstudy.save()
            return redirect('users:workstudy_list')
    else:
        form = WorkstudyForm()
    return render(request, 'users/workstudy_form.html', {'form': form, 'action': 'Add'})

@admin_required
def workstudy_edit(request, pk):
    workstudy = get_object_or_404(User, pk=pk, is_workstudy=True)
    if request.method == 'POST':
        form = WorkstudyForm(request.POST, instance=workstudy)
        if form.is_valid():
            form.save()
            return redirect('users:workstudy_list')
    else:
        form = WorkstudyForm(instance=workstudy)
    return render(request, 'users/workstudy_form.html', {'form': form, 'action': 'Edit'})


@admin_required
def workstudy_delete(request, pk):
    workstudy = get_object_or_404(User, pk=pk, is_workstudy=True)
    if request.method == 'POST':
        workstudy.delete()
        return redirect('users:workstudy_list')
    return render(request, 'users/workstudy_confirm_delete.html', {'workstudy': workstudy})


@admin_required
def workstudy_reset_password(request, pk):
    workstudy = get_object_or_404(User, pk=pk, is_workstudy=True)
    workstudy.set_password('0akl@ndL1br@ry2025')
    workstudy.must_change_password = True
    workstudy.save()
    return redirect('users:workstudy_list')

def admin_only(request):
    return render(request, 'users/admin_only.html')