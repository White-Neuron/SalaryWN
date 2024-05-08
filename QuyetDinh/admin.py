from django.contrib import admin
# from Payroll.admin import *
from .models import *
# Register your models here.

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
admin.site.register(ChucVu, ChucVuAdmin)
admin.site.register(CapBac, CapBacAdmin)

admin.site.register(HeSoLuong, HeSoLuongAdmin)