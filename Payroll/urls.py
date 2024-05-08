from django.contrib import admin 
from django.urls import path, include
from .views import *
from .models import *
urlpatterns = [
    path('send_salary_email/<int:bangluong_id>/', send_salary_email, name='send_email'),
    # path('import_excel/', import_nguoild, name='Payroll_nguoild_import_excel'),
    # path('admin/Payroll/', include('Payroll.urls')),
    # path('import_nguoild', import_nguoild, name='import_nguoild'),

] 
