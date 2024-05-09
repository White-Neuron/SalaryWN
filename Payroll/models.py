from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError
import pandas as pd
from QuyetDinh.models import *

class GioLam(models.Model):
    THANG_CHOICE=[
        (1, 1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12),
    ]
    thang = models.IntegerField(choices=THANG_CHOICE, null=True, blank=True, verbose_name="Lương tháng")
    quyetdinh = models.ForeignKey(QuyetDinhLuong, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quyết định tháng')
    mnv = models.CharField(max_length=10, null=True, blank=True, verbose_name='MNV')
    sogio = models.FloatField(null=True, blank=True, verbose_name='Số giờ làm việc')
    # sogio = models.FloatField(default=0.0, verbose_name='Số giờ làm việc', null=True, blank=True)
    date = models.DateField(null=True, blank=True, verbose_name='Ngày làm việc')

    def save(self, *args, **kwargs):
        self.thang = self.date.month
        if self.thang:
            try:
                self.quyetdinh = QuyetDinhLuong.objects.get(month=self.thang)
            except:
                self.quyetdinh = QuyetDinhLuong.objects.filter().first()
        super(GioLam, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Giờ Làm'
        verbose_name = 'Giờ Làm'
    
    def __str__(self):
        return self.mnv




class NguoiLD(models.Model):
    mnv = models.CharField(max_length=10, verbose_name='MNV')
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Tên', null=True, blank=True)
    # cap = models.ForeignKey(HeSoLuong, on_delete=models.SET_NULL, verbose_name='Cấp bậc', null=True, blank=True)
    HD_CHOICE=[
        ('Toàn thời gian', 'Toàn thời gian'),
        ('Bán thời gian', 'Bán thời gian'),
        ('Thực tập sinh', 'Thực tập sinh')
    ]
    loaihd = models.CharField(max_length=20, choices = HD_CHOICE, verbose_name = 'Loại hợp đồng')
    chucvu = models.ForeignKey(ChucVu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Chức vụ')


    def save(self, *args, **kwargs):
        try:
            bl = BangLuong.objects.get(mnv = self)
        except:
            bl = BangLuong(mnv = self)
            bl.save()
        super(NguoiLD, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Người Lao Động'


    def __str__(self):
        return str(self.mnv)


class BangLuong(models.Model):
    mnv = models.ForeignKey(NguoiLD, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Mã nhân viên')
    cap = models.ForeignKey(HeSoLuong, on_delete=models.SET_NULL, verbose_name='Cấp bậc', null=True, blank=True)
    THANG_CHOICE=[
        (1, 1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12),
    ]
    month = models.IntegerField(choices=THANG_CHOICE, null=True, blank=True, verbose_name='Lương tháng')
    sogio = models.FloatField(default=0.0, verbose_name='Số giờ làm việc', null=True, blank=True)
    luong = models.IntegerField(null=True, blank=True, verbose_name='Lương')
    
    qdluong = models.ForeignKey(QuyetDinhLuong, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quyết định lương')
    qdbac = models.ForeignKey(QuyetDinhTangBac, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quyết định tăng bậc')

    class Meta:
        verbose_name_plural = 'Thông Tin Lương'


    def __str__(self):
        s = "THÁNG " + str(self.month)
        return s

    def save(self, *args, **kwargs):
        try:
            self.qdluong = QuyetDinhLuong.objects.filter().last()
        except:
            return None
        try:
            self.qdbac = QuyetDinhTangBac.objects.filter(mnv = self.mnv).first()
        except:
            return None
        if self.month:
            try:
                self.quyetdinh = QuyetDinhLuong.objects.get(month=self.thang)
            except:
                self.quyetdinh = QuyetDinhLuong.objects.filter().last()
                print(self.quyetdinh)
        if self.cap and self.quyetdinh:       
            if self.mnv.loaihd == 'Thực tập sinh':
                hsluong = HeSoLuong.objects.filter(loaibac=self.cap.loaibac, bac = self.cap.bac).first()
                hsluong.manhour = 1200000 / 8 / 8
                # print(hsluong.manhour)
                hsluong.hsltheocap = 1
                self.quyetdinh.hesopt = 1
                self.luong = self.sogio * hsluong.manhour * hsluong.hsltheocap * self.quyetdinh.hesopt
                self.luong = min(self.luong, 1200000)
            else:
                hsluong = HeSoLuong.objects.filter(loaibac=self.cap.loaibac, bac = self.cap.bac).first()
                # print(hsluong)
                if self.mnv.loaihd == 'Toàn thời gian':
                    hsluong.manhour = hsluong.luongcoso / 26 / 8
                    self.luong = self.sogio * hsluong.manhour * hsluong.hsltheocap
                else: 
                    hsluong.manhour = hsluong.luongcoso / 26 / 8
                    self.luong = self.sogio * hsluong.manhour * hsluong.hsltheocap * self.quyetdinh.hesopt
                # print(self.luong)
                if self.mnv.chucvu:
                    self.luong += self.mnv.chucvu.thuong
            self.luong = int (round(self.luong, -4))
        super(BangLuong, self).save(*args, **kwargs)
        pass  

    def _cap(self):
        try:
            qd = QuyetDinhTangBac.objects.filter(mnv = self.mnv, bac_moi = self.cap).first()
            s = str(self.cap) + " (" + str(qd) + ")"
            return s 
        except:
            return str(self.cap) + " (" + ")"
    _cap.short_description = 'Cấp bậc'

    def _luong(self):
        try:
            # print(self.luong)
            return "{:,.0f} đồng".format(self.luong)
        except:
            return None
    _luong.short_description = 'Lương'

    def _luongcoso(self):
        try:
            return "{:,.0f} đồng".format(self.cap.luongcoso)
        except:
            return None
    _luongcoso.short_description = 'Lương cơ sở'


    def luong_in_words(self):
        try:
            number = int(self.luong)
            # 5,055,020 : năm triệu không trăm năm lăm nghìn không trăm hai mươi
            # 5,005,002 : năm triệu không trăm linh năm nghìn không trăm linh hai
            don_vi = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
            chu_so_hang_chuc = ["linh", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi",
                                "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
            hang_tram = ["", "trăm"]
            don_vi_khoang= ["","nghìn","triệu","tỷ","nghìn tỷ","triệu tỷ","tỷ tỷ","nghìn tỷ tỷ","triệu tỷ tỷ","tỷ tỷ tỷ"]
            def splitnumber(number):
                array=[]
                number=str(number)
                #cắt thành 3 số 1 lần rồi thêm vào mảng
                while len(number)>3:
                    array.append(number[-3:])
                    number=number[:-3]
                array.append(number)
                return array
            def read3digits(number):
        
                number=str(number)
                tram=int(number[0])
                chuc=int(number[1])
                donvi=int(number[2])
                ketqua=""
                ketqua+=don_vi[tram]+" "+hang_tram[1]+" "
                if chuc==0 and donvi==0:
                    return ketqua
                if chuc==0 and donvi!=0:
                    ketqua= ketqua+"linh "+don_vi[donvi]
                if chuc!=0 and donvi!=0:
                    ketqua= ketqua+chu_so_hang_chuc[chuc]+" "+don_vi[donvi]
                if chuc!=0 and donvi==0:
                    ketqua= ketqua+chu_so_hang_chuc[chuc]
                if "mươi bốn" in ketqua:
                    ketqua=ketqua.replace("mươi bốn","mươi tư")
                if "mươi một" in ketqua:
                    ketqua=ketqua.replace("mươi một","mươi mốt")
                return ketqua
            def read1or2digits(number):
                result=""
                if len(number)==1:
                    result+=don_vi[int(number[0])]
                else:
                    if number[0]=="1":
                        result="mười "+don_vi[int(number[1])]
                    else:
                        result=chu_so_hang_chuc[int(number[0])]+" "+don_vi[int(number[1])]
                return result
            def readnumber(number):
                result=""
                array=splitnumber(number)
                #đọc từng phần tử trong mảng
                for i in range(len(array)):
                    if len(array[i])==1 or len(array[i])==2:
                        result=read1or2digits(array[i])+" "+don_vi_khoang[i]+" "+result
                    else:
                        result=read3digits(array[i])+" "+don_vi_khoang[i]+" "+result
                result=result+"đồng"
                result = ' '.join(result.split())
                if "không trăm đồng" in result:
                    result=result.replace("không trăm đồng","đồng")
                return result 
            return readnumber(number)
        
        except:
            return None
    luong_in_words.short_description = 'Bằng chữ'

    def _giangaycong(self):
        try:
            return "{:,.0f} đồng".format(self.cap.manhour)
        except:
            return None
        
    _giangaycong.short_description = 'Giá một ngày công'


    def bang_luong(self):
        try:
            data = {
                "Thông tin": ["Lương tháng","Mã Nhân Viên", "Cấp", "Hệ số Lương theo cấp", 
                              "Lương cơ sở", "Loại hoạt động", 
                            "Số giờ làm việc", "Tổng lương", "Bằng chữ"],
                "Giá trị": [self.month, self.mnv, self.cap, self.cap.hsltheocap, 
                            self._luongcoso(), self.mnv.loaihd, 
                            self.sogio, self._luong(), self.luong_in_words()]
            }
            df = pd.DataFrame(data)

            html_table = df.to_html(index=False, header=True, classes='table table-striped', border=2)

            return format_html(html_table)
        except:
            return None
    bang_luong.short_description = 'Bảng Lương theo tháng' 

