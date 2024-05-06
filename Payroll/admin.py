from django.contrib import admin
from .models import *
from import_export import resources, fields
# from import_export.fields import FileChoiceField
from import_export.admin import ImportExportModelAdmin, ImportMixin, ImportForm, ConfirmImportForm
from django import forms
from django.http import HttpRequest, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
import pandas as pd

# class CapBacAdmin(admin.ModelAdmin):
#     list_display = ['cb','name', 'heso', 'qd']
#     list_filter = ['qd']
#     #TODO: inline 
#     inlines = [HeSoLuongInLine]

class CapBacInline(admin.TabularInline):
    model = CapBac
    extra = 0

class HeSoLuongInLine(admin.TabularInline):
    model = HeSoLuong
    extra = 0
    fieldsets= (
        (
            None, {
            # "classes": ["collapse"],
            "fields": ['hsltheocap', 'loaibac','bac', 'muctang', '_luongcoso']
        }),
    )
    readonly_fields = ['loaibac','bac', 'qd', 'muctang', '_luongcoso', 'luongcoso', 'manhour']
    can_delete = False
    max_num=0
    
    
class CapBacAdmin(admin.ModelAdmin):
    readonly_fields = ['cb', 'name', 'qd']
    list_display = ['cb','name', 'heso', 'qd']
    list_filter = ['qd']
    readonly_fields = ['cb', 'name', 'qd']
    #TODO: inline 
    inlines = [HeSoLuongInLine]

class ChucVuInline(admin.TabularInline):
    model = ChucVu
    extra = 0

class ChucVuAdmin(admin.ModelAdmin):
    list_display = ['kh', 'name', 'thuong', 'qd']
    list_filter = ['qd']


    
class HeSoLuongAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'hsltheocap','qd']
    readonly_fields = ['__str__','qd','loaibac','bac','muctang', '_luongcoso', '_manhour']
    list_filter = ['qd']
    fieldsets= (
        (
            None, {
            # "classes": ["collapse"],
            "fields": ['__str__', 'qd', 'hsltheocap', 'muctang', '_luongcoso']
        }),
    )
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False



class NguoiLDResource(resources.ModelResource):
    mnv = fields.Field(attribute='mnv', column_name='Mã nhân viên')
    email = fields.Field(attribute='email', column_name='Email')
    loaihd = fields.Field(attribute='loaihd', column_name='Loại hợp đồng')
    songay = fields.Field(attribute='songay', column_name='Số ngày làm việc')

    class Meta:
        model = NguoiLD
        fields = ('mnv', 'email', 'loaihd', 'songay',)
        import_id_fields = ['mnv',]



class NguoiLDAdmin(admin.ModelAdmin):
    resource_class = NguoiLDResource
    list_display = ['mnv','name', 'cap', 'chucvu', 'loaihd', 'sogio', '_luong', 'send_button']
    readonly_fields = ['_cap','sogio','loaihd', "_luong", 'quyetdinh', 'luong', 'luong_in_words', 'bang_luong']
    list_filter = ['quyetdinh', 'thang']
    fieldsets= (
        ("Thông tin cơ bản", {
            "fields": ["mnv","name", "email", "chucvu"]
        }),
        ("Thông tin lương", {
            "fields": ["_cap", "loaihd", "sogio", "thang", "quyetdinh", "_luong", "luong_in_words"]
        })
    )
    actions = ['send_email']

    def send_email(self, request, queryset):
        for obj in queryset:
            try:
                salary_table = obj.bang_luong()
                subject = 'Bảng lương'
                from_email = 'hostt4569@gmail.com'  
                to_email = [obj.email]
                html = render_to_string('email_template.html', {'salary_table': salary_table})
                send_mail(subject, '', from_email, to_email, html_message=html)
                self.message_user(request, 'Email đã được gửi thành công')
            except Exception as e:
                self.message_user(request, f"Có lỗi xảy ra: {str(e)}", level='error')
        return HttpResponseRedirect(reverse("admin:Payroll_nguoild_changelist"))

    def send_button(self, obj):
        send_url = f'/admin/Payroll/send_salary_email/{obj.id}' 
        return format_html('<a class="button" href="{}">Send Email</a>', send_url)
    send_button.allow_tags = True
    send_button.short_description = 'Send Email'

    # def send_email_actions(self, request, queryset):



class GioLamAmin(admin.ModelAdmin):
    list_filter = ['mnv', 'thang']
    list_display = ['mnv', 'sogio','date', 'thang']

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request):
        return False

admin.site.register(ChucVu, ChucVuAdmin)
admin.site.register(GioLam, GioLamAmin)
admin.site.register(CapBac, CapBacAdmin)

admin.site.register(HeSoLuong, HeSoLuongAdmin)
admin.site.register(NguoiLD, NguoiLDAdmin)
