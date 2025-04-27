from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('upload/', views.upload_reference, name='upload_reference'),
    path('map-columns/', views.process_reference_mapping, name='process_reference_mapping'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('process-mapping/', views.process_reference_mapping, name='process_reference_mapping'),

    path('', views.reference_list, name='reference_list'),
    path('add/', views.reference_add, name='reference_add'),
    path('edit/<int:student_id>/', views.reference_edit, name='reference_edit'),
    path('delete/<int:student_id>/', views.reference_delete, name='reference_delete'),
    path('delete/all/', views.reference_delete_all, name='reference_delete_all'),
    path('<str:letter>/', views.reference_list, name='reference_list_letter'),
]
