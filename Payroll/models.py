from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError
import pandas as pd



class QuyetDinh(models.Model): #quyết định đc đặt dựa theo tháng tính lương
    date = models.DateField(null=True, blank=True,verbose_name='Ngày ban hành')
    month = models.IntegerField(null=True, blank=True, verbose_name='Quyết định tháng')
    hesopt = models.FloatField(default=0.8, verbose_name='Hệ số part time')
    luongcoso = models.IntegerField(default=1800000,verbose_name='Lương cơ sở')
    hsphucap = models.FloatField(default=0.0, verbose_name='Hệ số phụ cấp')
    hsdieuchinh = models.FloatField(default=0.9, verbose_name='Hệ số điều chỉnh')
    bhyt = models.FloatField(default=0.235, verbose_name='Bảo hiểm y tế')
    

    def save(self, *args, **kwargs):
        self.month = self.date.month
        super(QuyetDinh, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quyết Định'
    def __str__(self):
        s = 'Quyết định tháng ' + str(self.month)
        return s
    

class CapBac(models.Model):
    qd = models.ForeignKey(QuyetDinh, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Quyết định')
    cb = models.CharField(
        max_length = 5,
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
    qd = models.ForeignKey(QuyetDinh, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Quyết định')
    # TODO: loaibac: CapBac, bac: int. __str__, xoa cap
    loaibac = models.ForeignKey(CapBac, on_delete=models.CASCADE, verbose_name='Loại bậc')
    bac = models.IntegerField(null=True, blank=True, verbose_name='Bậc')
    hsltheocap = models.FloatField(default=1.0, verbose_name='Hệ số lương theo cấp bậc', null=True, blank=True)
    hsphucap = models.FloatField(null=True, blank=True, verbose_name='Hệ số phụ cấp')
    luongcoso = models.IntegerField(null=True, blank=True, verbose_name='Lương cơ sở')
    hsdieuchinh = models.FloatField(null=True, blank=True, verbose_name='Hệ số điều chỉnh')
    bhyt = models.FloatField(null=True, blank=True, verbose_name='Bảo hiểm y tế')
    giangaycong = models.IntegerField(null=True, blank=True, verbose_name='Giá một ngày công')

    def save(self, *args, **kwargs):
        self.hsphucap = self.qd.hsphucap
        self.luongcoso = self.qd.luongcoso
        self.hsdieuchinh = self.qd.hsdieuchinh
        self.bhyt = self.qd.bhyt
        self.giangaycong = round(((self.hsltheocap+self.hsphucap)*self.luongcoso*(1+self.hsdieuchinh+self.bhyt)/26),0)
        super(HeSoLuong, self).save(*args, **kwargs)
        
        

    class Meta:
         verbose_name_plural = 'Hệ Số Lương'

    def __str__(self):
        return str(self.loaibac.cb) + str(self.bac)
    
    def _giangaycong(self):
        try:
            return "{:,.0f} đồng".format(self.giangaycong)
        except:
            return None
        
    _giangaycong.short_description = 'Giá một ngày công'
    def _luongcoso(self):
        try:
            return "{:,.0f} đồng".format(self.luongcoso)
        except:
            return None
    _luongcoso.short_description = 'Lương cơ sở'
    

class NguoiLD(models.Model):
    mnv = models.CharField(max_length=10, verbose_name='MNV')
    email = models.EmailField(null=True, blank=True)
    cap = models.ForeignKey(HeSoLuong, on_delete=models.DO_NOTHING, verbose_name='Cấp', null=True, blank=True)
    HD_CHOICE=[
        ('Toàn thời gian', 'Toàn thời gian'),
        ('Bán thời gian', 'Bán thời gian'),
    ]
    loaihd = models.CharField(max_length=20, choices = HD_CHOICE, verbose_name = 'Loại hợp đồng')
    songay = models.IntegerField(verbose_name='Số ngày đi làm', null=True, blank=True)
    luong = models.IntegerField(null=True, blank=True, verbose_name='Lương')
    THANG_CHOICE=[
        (1, 1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12),
    ]
    thang = models.IntegerField(choices=THANG_CHOICE, null=True, blank=True, verbose_name="Lương tháng")
    quyetdinh = models.ForeignKey(QuyetDinh, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quyết định tháng')

    def save(self, *args, **kwargs):
        if self.thang:
            try:
                self.quyetdinh = QuyetDinh.objects.get(month=self.thang)
            except:
                self.quyetdinh = QuyetDinh.objects.filter().first()
                

        if self.cap:
            hsluong = HeSoLuong.objects.filter(loaibac=self.cap.loaibac).first()
            if self.loaihd == 'Toàn thời gian':
                self.luong = round((hsluong.giangaycong)*float(self.songay),0)
            else: self.luong = round(hsluong.giangaycong*float(self.songay)*self.quyetdinh.hesopt,0)
        super(NguoiLD, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Người Lao Động'

    def __str__(self):
        return str(self.mnv)
    
        
    
    # def luong_in_words(self):
    #     try:
    #         luong_words = num2words(self.luong, lang='vi')
    #         luong_words = luong_words.replace("point", "phẩy")
    #         # luong_words = luong_words.replace("lẻ", "không trăm")
    #         return luong_words
    #     except:
    #         return None
    # luong_in_words.short_description = 'Bằng chữ'
        
    def _luong(self):
        try:
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
            num = int(self.luong)
            # 5,055,020 : năm triệu không trăm năm lăm nghìn không trăm hai mươi
            # 5,005,002 : năm triệu không trăm linh năm nghìn không trăm linh hai
            num2words_less_10 = {0 : "không ", 1 : "một ", 2 : "hai ", 3 : "ba ", 4 : "bốn ", 
                                 5 : "năm ", 6 : "sáu ", 7 : "bảy ", 8 : "tám ", 9 : "chín "}
            tens_power = ["trăm ", "nghìn ", "triệu ", 'mươi ', "linh ", 'mười ', 'mốt ']
            s=''
            if 1000000 <= num < 10000000:
          # 9,511,087 : chín triệu năm trăm mười một nghìn không trăm tám mươi bảy
          # 9,521,087 : chín triệu năm trăm hai mươi mốt nghìn không trăm tám mươi bảy
          # 9,504,087 : chín triệu năm trăm linh bốn nghìn không trăm tám mươi bảy
          # 9,521,087 : chín triệu năm trăm hai mươi mốt nghìn không trăm tám mươi bảy
                n = int(num / 1000000) #9
                s += num2words_less_10[n]
                s += tens_power[2] #triệu
                num = num-n*1000000 # 511,087
                n = int(num/100000) #5
                s += num2words_less_10[n]
                s += tens_power[0] #trăm
                num =num -n*100000 # 11,087
                n = int(num/10000) #1
                n1 = n
                if n==0:
                    s += tens_power[4] #linh
                elif n==1:
                    s += tens_power[5] #mười
                else:
                    s += num2words_less_10[n]
                    s += tens_power[3] #mươi

                num = num-n*10000 #1,087
                n = int(num/1000) #1 mười một, hai mươi mốt
                if n!=1: #mười hap, hai mươi hai
                    s += num2words_less_10[n]
                if n==1 and n1!=1: #hai mươi mốt
                    s += tens_power[6]
                if n==1 and n1==1:
                    s+= num2words_less_10[n]
                s += tens_power[1] #nghìn
                num = num-n*1000 #87
                n = int(num/100) #0
                s += num2words_less_10[n]
                s += tens_power[0] #trăm
                num = num-n*100 #21
                n = int(num/10) #2
                if n==0:
                    s += tens_power[4] #linh
                elif n==1:
                    s += tens_power[5] #mười
                else:
                    s += num2words_less_10[n]
                    s += tens_power[3] #mươi
                num = num-n*10 #1
                if num!=1 and num!=0: #mười hai, hai mươi hai
                    s += num2words_less_10[num]
                if num==1 and n!=1: #hai mươi mốt
                    s += tens_power[6]
                if num==1 and n==1:
                    s+= num2words_less_10[num]
                # n = int(num/10)
                # num
            if num >= 10000000: #21,583,040
                n = int(num/10000000) 
                n1=n #2
                if n==1:
                    s += tens_power[5] #mười
                else:
                    s += num2words_less_10[n]
                    s += tens_power[3] #mươi
                num = num-n*10000000
                n = int(num / 1000000) #1
                if n!=1 and n!=0: #mười hai, hai mươi hai
                    s += num2words_less_10[num]
                if n==1 and n1!=1: #hai mươi mốt
                    s += tens_power[6]
                if n==1 and n1==1:
                    s+= num2words_less_10[num]
                s += tens_power[2] #triệu
                num = num-n*1000000 # 514,087
                n = int(num/100000) #5
                s += num2words_less_10[n]
                s += tens_power[0] #trăm
                num =num -n*100000 # 14,087
                n = int(num/10000) #1
                n1 = n
                if n==0:
                    s += tens_power[4] #linh
                elif n==1:
                    s += tens_power[5] #mười
                else:
                    s += num2words_less_10[n]
                    s += tens_power[3] #mươi

                num = num-n*10000 #4,087
                n = int(num/1000) #4
                if n!=1: #mười hap, hai mươi hai
                    s += num2words_less_10[n]
                if n==1 and n1!=1: #hai mươi mốt
                    s += tens_power[6]
                if n==1 and n1==1:
                    s+= num2words_less_10[n]
                s += tens_power[1] #nghìn
                num = num-n*1000 #87
                n = int(num/100) #0
                s += num2words_less_10[n]
                s += tens_power[0] #trăm
                num = num-n*100 #87
                n = int(num/10) #8
                if n==0:
                    s += tens_power[4] #linh
                elif n==1:
                    s += tens_power[5] #mười
                else:
                    s += num2words_less_10[n]
                    s += tens_power[3] #mươi
                num = num-n*10 #7
                if num!=1 and num!=0: #mười hai, hai mươi hai
                    s += num2words_less_10[num]
                if num==1 and n!=1: #hai mươi mốt
                    s += tens_power[6]
                if num==1 and n==1:
                    s+= num2words_less_10[num]

            return s + ' đồng'
        except:
            return None
    luong_in_words.short_description = 'Bằng chữ'

    def _giangaycong(self):
        try:
            return "{:,.0f} đồng".format(self.cap.giangaycong)
        except:
            return None
        
    _giangaycong.short_description = 'Giá một ngày công'

            

    def bang_luong(self):
        try:
        # Tạo DataFrame từ dữ liệu lương
            data = {
                "Thông tin": ["Mã Nhân Viên", "Cấp", "Hệ số Lương theo cấp", "Hệ số phụ cấp", "Lương cơ sở", 
                            "Hệ số điều chỉnh", "Bảo hiểm y tế", "Giá một ngày công", "Loại hoạt động", 
                            "Số ngày làm việc", "Tổng lương", "Bằng chữ", "Công thức tính lương"],
                "Giá trị": [self.mnv, self.cap, self.cap.hsltheocap, self.cap.hsphucap, self._luongcoso(), 
                            self.cap.hsdieuchinh, self.cap.bhyt, self._giangaycong(), self.loaihd, 
                            self.songay, self._luong(), self.luong_in_words(), "[(hệ số lương theo cấp + hế số phụ cấp) x lương cơ sở x (1 + hệ số điều chỉnh + bảo hiểm y tế) : 26] x số ngày làm việc x hệ số part time(0.8)"]
            }
            df = pd.DataFrame(data)

            # Vẽ bảng lương
            html_table = df.to_html(index=False, header=True, classes='table table-striped', border=2)

            return html_table
        except:
            return None
    bang_luong.short_description = 'Bảng Lương'



class ImportNguoiLD(models.Model):

    class Meta:
        verbose_name_plural = 'Import Người Lao Động'
        verbose_name = 'Import Người Lao Động'
    pass