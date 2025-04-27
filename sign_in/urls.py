from django.urls import path
from . import views

app_name = 'sign_in'

urlpatterns = [
    path('', views.home, name='home'),
    path('manage/', views.manage_page, name='manage'),
    path('sign-out/<int:record_id>/', views.sign_out_student, name='sign_out_student'),
    path('partials/current/', views.current_students_partial, name='current_students_partial'),
    path('partials/recent/', views.recently_left_partial, name='recently_left_partial'),
    path('undo/<int:record_id>/', views.undo, name='undo'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
]