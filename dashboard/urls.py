from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.data_page, name='data'),
    path('export/', views.export_records, name='export_records'),
]