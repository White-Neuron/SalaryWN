from django.contrib import admin
from django.http import HttpRequest
from .models import *
from .forms import *
from django.contrib import messages


class ImportNVAdmin(admin.ModelAdmin):
    change_list_template= 'admin/import_nguoild_change_list.html'

    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        view.context_data['submit_form'] = ImportNguoiLDForm()
        self.message_user(
            args[0],
            args[0].session.get('message', ''),
            level= messages.ERROR if args[0].session.get('status', '') == 'error' else messages.SUCCESS,
        )
        view.context_data['message']= args[0].session.get('message', '')
        return view

    

admin.site.register(ImportNhanVien, ImportNVAdmin)

class ImportGioAdmin(admin.ModelAdmin):
    change_list_template= 'admin/import_giolam_change_list.html'

    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        view.context_data['submit_form'] = ImportGioLamForm()
        self.message_user(
            args[0],
            args[0].session.get('message', ''),
            level= messages.ERROR if args[0].session.get('status', '') == 'error' else messages.SUCCESS,
        )
        return view
    

admin.site.register(ImportGio, ImportGioAdmin)