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



    

class CapBac(models.Model):
    qd = models.ForeignKey(QuyetDinhLuong, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Quyết định')
    cb = models.CharField(
        max_length = 20,
        verbose_name='Ký hiệu', null=True, blank=True
    )
    name = models.CharField(max_length=20,null=True, blank=True, verbose_name='Tên')
    heso = models.IntegerField(null=True, blank=True, verbose_name='Tổng Bậc')

    def save(self, *args, **kwargs):
        super(CapBac, self).save(*args, **kwargs)
        
        if self.cb:
            for i in range (1, self.heso+1):
                try: 
                    hsl=HeSoLuong.objects.get(qd = self.qd, loaibac=self, bac=i)
                except:
                    hsl=HeSoLuong(qd = self.qd, loaibac = self, bac=i)
                    hsl.save()

        cap = CapBac.objects.get(qd = self.qd, cb = self.cb)
        tongbac=HeSoLuong.objects.filter(qd = self.qd, loaibac=cap).count()
        
        if (cap.heso < tongbac):
            for i in range(cap.heso+1, tongbac+1):
                HeSoLuong.objects.get(qd = self.qd, loaibac=cap, bac = i).delete()
        
    class Meta:
         verbose_name_plural = 'Cấp Bậc'
    
    def __str__(self):
        return self.cb
    

class HeSoLuong(models.Model):
    qd = models.ForeignKey(QuyetDinhLuong, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Quyết định')
    # TODO: loaibac: CapBac, bac: int. __str__, xoa cap
    loaibac = models.ForeignKey(CapBac, on_delete=models.CASCADE, verbose_name='Loại bậc')
    bac = models.IntegerField(null=True, blank=True, verbose_name='Bậc')
    hsltheocap = models.FloatField(default=1.0, verbose_name='Hệ số lương theo cấp bậc', null=True, blank=True)
    muctang = models.FloatField(null=True, blank=True, verbose_name='Mức tăng')
    luongcoso = models.IntegerField(null=True, blank=True, verbose_name='Lương cơ sở')
    manhour = models.IntegerField(null=True, blank=True, verbose_name='Lương cơ sở theo giờ')

    def save(self, *args, **kwargs):
        self.muctang = self.qd.muctang
        self.luongcoso = (self.qd.luongcoso) * (1+self.qd.muctang)
        # self.giagiocong = round(((self.giangaycong)/(self.qd.sogio)),0)
        super(HeSoLuong, self).save(*args, **kwargs)
        
        

    class Meta:
         verbose_name_plural = 'Hệ Số Lương'

    def __str__(self):
        return str(self.loaibac.cb) + str(self.bac)
    
    def _manhour(self):
        try:
            return "{:,.0f} đồng".format(self.manhour)
        except:
            return None
        
    _manhour.short_description = 'Lương cơ sở theo giờ'
    def _luongcoso(self):
        try:
            return "{:,.0f} đồng".format(self.luongcoso)
        except:
            return None
    _luongcoso.short_description = 'Lương cơ sở'
    
class ChucVu(models.Model):
    qd = models.ForeignKey(QuyetDinhLuong, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Quyết định')
    kh = models.CharField(
        max_length = 20,
        verbose_name='Ký hiệu', null=True, blank=True
    )
    name = models.CharField(max_length=20,null=True, blank=True, verbose_name='Tên')
    thuong = models.IntegerField(null=True, blank=True, verbose_name='Thưởng phụ cấp')
        
    class Meta:
         verbose_name_plural = 'Chức Vụ'
    
    def __str__(self):
        return self.kh
    

class QuyetDinhTangBac(models.Model):
    mnv = models.ForeignKey('Payroll.NguoiLD', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Mã nhân viên')
    date = models.DateField(null=True, blank=True, verbose_name='Ngày quyết định')
    bac_cu = models.ForeignKey(HeSoLuong, on_delete=models.SET_NULL, null=True, blank=True, related_name='bac_cu_quyetdinh_set', verbose_name='Bậc cũ')
    bac_moi = models.ForeignKey(HeSoLuong, on_delete=models.SET_NULL, null=True, blank=True, related_name='bac_moi_quyetdinh_set', verbose_name='Bậc mới')

    def save(self, *args, **kwargs):
        nguoild_model = apps.get_model('Payroll', 'BangLuong')
        nguoild = nguoild_model.objects.filter(mnv=self.mnv).last()
        # print(nguoild.thang)
        self.bac_cu = nguoild.cap
        nguoild.cap = self.bac_moi
        nguoild.save()
        
        super(QuyetDinhTangBac, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Quyết Định Tăng Bậc'
    def __str__(self):
        s = 'Quyết định ngày ' + str(self.date) 
        return s