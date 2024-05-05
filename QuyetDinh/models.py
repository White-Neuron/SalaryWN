from django.db import models
# from ImportData.models import *
# Create your models here.

class QuyetDinhLuong(models.Model): #quyết định đc đặt dựa theo tháng tính lương
    date = models.DateField(null=True, blank=True,verbose_name='Ngày ban hành')
    month = models.IntegerField(null=True, blank=True, verbose_name='Quyết định tháng')
    hesopt = models.FloatField(default=0.8, verbose_name='Hệ số part time')
    luongcoso = models.IntegerField(default=1800000,verbose_name='Lương cơ sở')
    muctang = models.FloatField(default=0.0, verbose_name='Mức tăng')
    

    def save(self, *args, **kwargs):
        self.month = self.date.month
        super(QuyetDinhLuong, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quyết Định Lương'
    def __str__(self):
        s = 'Quyết định số ' + str(self.month)
        return s
    
from django.apps import apps



class QuyetDinhTangBac(models.Model):
    mnv = models.ForeignKey('Payroll.NguoiLD', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mã nhân viên')
    date = models.DateField(null=True, blank=True, verbose_name='Ngày quyết định')
    bac_cu = models.ForeignKey('Payroll.HeSoLuong', on_delete=models.SET_NULL, null=True, blank=True, related_name='bac_cu_quyetdinh_set', verbose_name='Bậc cũ')
    bac_moi = models.ForeignKey('Payroll.HeSoLuong', on_delete=models.SET_NULL, null=True, blank=True, related_name='bac_moi_quyetdinh_set', verbose_name='Bậc mới')

    def save(self, *args, **kwargs):
        nguoild_model = apps.get_model('Payroll', 'NguoiLD')
        nguoild = nguoild_model.objects.filter(mnv=self.mnv).first()
        self.bac_cu = nguoild.cap
        nguoild.cap = self.bac_moi
        nguoild.save()
        super(QuyetDinhTangBac, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Quyết Định Tăng Bậc'
    def __str__(self):
        s = 'Quyết định ngày ' + str(self.date) 
        return s