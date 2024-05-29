from django.contrib import admin 
from django.urls import path, include
from .views import *
from .models import *
urlpatterns = [
    path('import_nguoild', import_nguoild, name='import_nguoild'),
    path('import_giolam', import_giolam, name='import_giolam'),
    # path('process_month_selection', process_month_selection, name='process_month_selection'),

] 
