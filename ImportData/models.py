from django.db import models
from Payroll.models import *
# Create your models here.

class ImportNhanVien(models.Model):

    class Meta:
        verbose_name_plural = 'Import Người Lao Động'
        verbose_name = 'Import Người Lao Động'
    


class ImportGio(models.Model):
    class Meta:
        verbose_name_plural = 'Import Giờ Làm'
        verbose_name = 'Import Giờ Làm'
    
    