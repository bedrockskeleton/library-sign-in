from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('force-password-change/', views.force_password_change, name='force_password_change'),
    path('workstudies/', views.workstudy_list, name='workstudy_list'),
    path('workstudies/add/', views.workstudy_add, name='workstudy_add'),
    path('workstudies/edit/<int:pk>/', views.workstudy_edit, name='workstudy_edit'),
    path('workstudies/delete/<int:pk>/', views.workstudy_delete, name='workstudy_delete'),
    path('workstudies/reset-password/<int:pk>/', views.workstudy_reset_password, name='workstudy_reset_password'),
    path('denied/', views.admin_only, name='admin_only'),
]
