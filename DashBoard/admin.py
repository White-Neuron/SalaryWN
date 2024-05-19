from django.contrib import admin

# Register your models here.
# from Base import admin
from django.http.request import HttpRequest
from .models import *
from Payroll.models import NguoiLD
from django.shortcuts import render
from django.utils.html import format_html

       
class ThongKeLuongAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_salary.html'
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True
    
    
class ThongKeGioLamAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list_giolam.html'
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

    

admin.site.register(ThongKeGioLam, ThongKeGioLamAdmin)
admin.site.register(ThongKeLuong, ThongKeLuongAdmin)

