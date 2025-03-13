from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.db.models import Sum, F, ExpressionWrapper, fields

# Create your views here.

def public(request):
    return render(request, "public.html")

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print([email, password])
        emailSuffix = ['oak.edu, myocu.oak.edu']
        if User.objects.filter(email=email).exists():
            user = auth.authenticate(email=email, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                return redirect('public')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect("login")
        else:
            messages.info(request, "Invalid email or password")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('public')