from django.contrib import admin 
from django.urls import path, include
# from .views import *
from .views import chart_summary, chart_summary_all, chart_giolam, chart_giolam_all, get_employees
urlpatterns = [
    
    path('api/salary/chart_summary/<str:mnv>/', chart_summary, name='chart_summary'),
    path('api/salary/chart_summary_all/', chart_summary_all, name='chart_summary_all'),
    path('api/giolam/chart_giolam/<str:mnv>/', chart_giolam, name='chart_giolam'),
    path('api/giolam/chart_giolam_all/', chart_giolam_all, name='chart_giolam_all'),
    path('api/get_employees/', get_employees, name= "get_employees"), 

] 
