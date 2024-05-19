from django.db import models
from Payroll.models import BangLuong
# Create your models here.


class ThongKeLuong(BangLuong):
    class Meta:
        verbose_name_plural = 'Thống Kê Lương'


class ThongKeGioLam(BangLuong):
    class Meta:
        verbose_name_plural = 'Thống Kê Giờ Làm'





