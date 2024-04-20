from django.contrib import admin
from .models import *
from import_export import resources, fields
# from import_export.fields import FileChoiceField
from import_export.admin import ImportExportModelAdmin, ImportMixin, ImportForm, ConfirmImportForm
from django import forms
from django.http import HttpResponseRedirect
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
    readonly_fields = ['loaibac','bac', 'qd', 'hsphucap', 'luongcoso', 'hsdieuchinh', 'bhyt', 'giangaycong']
    can_delete = False
    max_num=0
    
    
class CapBacAdmin(admin.ModelAdmin):
    readonly_fields = ['cb', 'name', 'qd']
    list_display = ['cb','name', 'heso', 'qd']
    list_filter = ['qd']
    # readonly_fields = ['cb', 'name', 'qd']
    #TODO: inline 
    inlines = [HeSoLuongInLine]

class QuyetDinhAdmin(admin.ModelAdmin):
    list_display = ['month', 'date', 'hesopt']
    readonly_fields = ['month']
    inlines = [CapBacInline, HeSoLuongInLine]
    
class HeSoLuongAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'hsltheocap', '_giangaycong','qd']
    readonly_fields = ['__str__','qd','loaibac','bac','hsphucap', '_luongcoso', 'hsdieuchinh', 'bhyt', '_giangaycong']
    list_filter = ['qd']
    fieldsets= (
        (
            None, {
            # "classes": ["collapse"],
            "fields": ['__str__', 'qd', 'hsltheocap', 'hsphucap', '_luongcoso', 'hsdieuchinh', 'bhyt', '_giangaycong']
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

# class CustomImpExp(ImportExportModelAdmin):
#     def select_field(self, request):
#         if request.method == 'POST':
#             selected_columns = request.POST.getlist('selected_columns')
#             # Xử lý selected_columns và ánh xạ chúng vào các trường trong model
#             # Sau đó tiến hành import dữ liệu
#             # Ví dụ:
#             # selected_columns = ['Mã Nhân Viên', 'Email', 'Loại Hợp Đồng', 'Số ngày']
#             # Các bạn có thể ánh xạ các cột này vào các trường tương ứng trong model và import dữ liệu

#             return HttpResponseRedirect(reverse('admin:index'))
#         else:
#             # Render template cho phép người dùng chọn cột tương ứng
#             # return render(request, 'admin/select_field.html', {'columns': columns_from_excel})
#             pass

# class FileChoiceField(forms.ChoiceField):
#     widget = forms.Select

#     def __init__(self, choices=(), *args, **kwargs):
#         super(FileChoiceField, self).__init__(choices=choices, *args, **kwargs)
#         self.choices = choices

# import openpyxl

# def get_columns(file_path):
#     columns = []
#     wb = openpyxl.load_workbook(file_path)
#     sheet = wb.active
#     for col in sheet.iter_cols(min_row=1, max_row=1, values_only=True):
#         columns.extend(col)
#     return columns

# class CustomImportForm(ImportForm):
#     # mnv = forms.ModelChoiceField(queryset=NguoiLD.objects.all(), required=True)
#     # email = forms.ModelChoiceField(queryset=NguoiLD.objects.all(), required=True)
#     # loaihd = forms.ModelChoiceField(queryset=NguoiLD.objects.all(), required=True)
#     # songay = forms.ModelChoiceField(queryset=NguoiLD.objects.all(), required=True)
#     mnv = FileChoiceField(choices=(), required=True)
#     email = FileChoiceField(choices=(), required=True)
#     loaihd = FileChoiceField(choices=(), required=True)
#     songay = FileChoiceField(choices=(), required=True)
    

#     def clean_import_file(self):
#         upload_file = self.cleaned_data['import_file']
#         # colums = upload_file.get_columns()
#         # columns = ["Mã nhân viên", "Email", "Loại hợp đồng", "Số ngày làm việc"]
#         columns = get_columns(upload_file)
#         self.fields['mnv'].choices = [(col, col) for col in columns]
#         self.fields['email'].choices = [(col, col) for col in columns]
#         self.fields['loaihd'].choices = [(col, col) for col in columns]
#         self.fields['songay'].choices = [(col, col) for col in columns]
#         return upload_file
    
#     def clean(self):
#         cleaned_data = super().clean()
#         self.clean_import_file()
#         return cleaned_data
    
# class CustomConfirmImportForm(ConfirmImportForm):
#     mnv = FileChoiceField(choices=(), required=True)
#     email = FileChoiceField(choices=(), required=True)
#     loaihd = FileChoiceField(choices=(), required=True)
#     songay = FileChoiceField(choices=(), required=True)
#     def __init__(self, *args, **kwargs):
#         super(CustomConfirmImportForm, self).__init__(*args, **kwargs)
#         self.clean_import_file_name()



    

    # def __init__(self, *args, **kwargs):
    #     super(CustomImportForm, self).__init__(*args, **kwargs)
    #     # columns = self.fields['import_file'].widget.get_import_columns()
    #     columns = ["Mã nhân viên", "Email", "Loại hợp đồng", "Số ngày làm việc"]
    #     self.fields['mnv'].choices = [(col, col) for col in columns]
    #     self.fields['email'].choices = [(col, col) for col in columns]
    #     self.fields['loaihd'].choices = [(col, col) for col in columns]
    #     self.fields['songay'].choices = [(col, col) for col in columns]



class NguoiLDAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = NguoiLDResource
    # import_form_class = CustomImportForm
    # confirm_form_class = CustomConfirmImportForm
    # list_display = ['mnv', 'cap', 'loaihd', 'songay', '_luong', 'send_email_buttom']
    # readonly_fields = ["_luong", 'quyetdinh', 'luong', 'luong_in_words', 'bang_luong']
    # list_filter = ['quyetdinh']
    # fieldsets= (
    #     ("Thông tin cơ bản", {
    #         "fields": ["mnv", "email"]
    #     }),
    #     ("Thông tin lương", {
    #         "fields": ["cap", "loaihd", "songay", "thang", "quyetdinh", "_luong", "luong_in_words"]
    #     })
    # )
    # actions = ['send_email']
    
    # def send_buttom(self, obj):
    #     send_url = f'/admin/Payroll/send_salary_email/{obj.id}' 
    #     return format_html('<a class="button" href="{}">Send Email</a>', send_url)
    # send_buttom.allow_tags = True
    # send_buttom.short_description = 'Select Project to Send Email'

    list_display = ['mnv', 'cap', 'loaihd', 'songay', '_luong', 'send_button']
    readonly_fields = ["_luong", 'quyetdinh', 'luong', 'luong_in_words', 'bang_luong']
    list_filter = ['quyetdinh']
    fieldsets= (
        ("Thông tin cơ bản", {
            "fields": ["mnv", "email"]
        }),
        ("Thông tin lương", {
            "fields": ["cap", "loaihd", "songay", "thang", "quyetdinh", "_luong", "luong_in_words"]
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
    send_button.short_description = 'Select Project to Send Email'

    # def send_email_actions(self, request, queryset):





admin.site.register(CapBac, CapBacAdmin)
admin.site.register(QuyetDinh, QuyetDinhAdmin)
admin.site.register(HeSoLuong, HeSoLuongAdmin)
admin.site.register(NguoiLD, NguoiLDAdmin)
