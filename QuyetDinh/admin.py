from django.contrib import admin
from Payroll.admin import *
from .models import *
# Register your models here.

class QuyetDinhLuongAdmin(admin.ModelAdmin):
    list_display = ['month', 'date', 'hesopt']
    readonly_fields = ['month']
    inlines = [ChucVuInline, CapBacInline, HeSoLuongInLine]

class QuyetDinhTangBacAdmin(admin.ModelAdmin):
    list_display = ['mnv','date', 'bac_cu', 'bac_moi']
    readonly_fields = ['bac_cu']
    pass


admin.site.register(QuyetDinhLuong, QuyetDinhLuongAdmin)
admin.site.register(QuyetDinhTangBac, QuyetDinhTangBacAdmin)