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

# remove admin interface for these models 
from admin_interface.models import Theme
admin.site.unregister(Theme)

# class CapBacAdmin(admin.ModelAdmin):
#     list_display = ['cb','name', 'heso', 'qd']
#     list_filter = ['qd']
#     #TODO: inline 
#     inlines = [HeSoLuongInLine]

class BangLuongInLine(admin.TabularInline):
    model = BangLuong
    extra = 0
    readonly_fields = ['bang_luong']
    fieldsets= (
        (
            None, {
            "fields" : ['bang_luong']
        }),
    )
    can_delete = False
    max_num = 0

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
    list_display = ['mnv','name', 'chucvu', 'loaihd']
    readonly_fields = ['loaihd', 'chucvu']
    # list_filter = ['quyetdinh', 'thang']
    fieldsets= (
        ("Thông Tin Cơ Bản", {
            "fields": ["mnv","name", "email", "chucvu"]
        }),
        # ("Bảng Lương", {
        #     # "fields": ["_cap", "loaihd", "sogio", "thang", "quyetdinh", "_luong"]
        #     "fields" : [BangLuongInLine]
        # }),
    )
    inlines = [BangLuongInLine]


class BangLuongAdmin(admin.ModelAdmin):
    change_form_template = 'admin/nguoild_change_form.html'
    list_display = ['mnv','cap','sogio', 'month', 'send_button']
    readonly_fields = ['_cap','luong','qdluong', 'qdbac','bang_luong']
    list_filter = ['mnv', 'month']
    fieldsets= (
        ("Thông tin lương", {
            "fields": ["mnv",'_cap', "month", "qdluong", "qdbac", "bang_luong"]
        }),
    )
    # inlines = [BangLuongInLine]
    actions = ['send_email']

    def send_email(self, request, queryset):
        for obj in queryset:
            try:
                salary_table = obj.bang_luong()
                subject = 'Bảng lương'
                from_email = 'hostt4569@gmail.com'  
                to_email = [obj.mnv.email]
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

admin.site.register(BangLuong, BangLuongAdmin)

class GioLamAmin(admin.ModelAdmin):
    list_filter = ['mnv', 'thang']
    list_display = ['mnv', 'sogio','date', 'thang']
    readonly_fields = ['mnv', 'thang','quyetdinh', 'sogio', 'date']

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(GioLam, GioLamAmin)
admin.site.register(NguoiLD, NguoiLDAdmin)
