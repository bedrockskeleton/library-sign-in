from django.urls import path
from sign_in import views

urlpatterns = [
    path('', views.public, name='public'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
