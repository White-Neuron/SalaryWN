from django.db import models
from Payroll.models import *
# Create your models here.

class ImportNhanVien(models.Model):

    class Meta:
        verbose_name_plural = 'Nhập dữ liệu Người Lao Động'
        verbose_name = 'Nhập dữ liệu Người Lao Động'
    


class ImportGio(models.Model):
    class Meta:
        verbose_name_plural = 'Nhập dữ liệu Giờ Làm'
        verbose_name = 'Nhập dữ liệu Giờ Làm'
    
    