from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError
import pandas as pd
from QuyetDinh.models import QuyetDinhLuong, QuyetDinhTangBac



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
class GioLam(models.Model):
    THANG_CHOICE=[
        (1, 1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12),
    ]
    thang = models.IntegerField(choices=THANG_CHOICE, null=True, blank=True, verbose_name="Lương tháng")
    quyetdinh = models.ForeignKey(QuyetDinhLuong, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quyết định tháng')
    mnv = models.CharField(max_length=10, null=True, blank=True, verbose_name='MNV')
    sogio = models.TimeField(null=True, blank=True, verbose_name='Số giờ làm việc')
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

class NguoiLD(models.Model):
    mnv = models.CharField(max_length=10, verbose_name='MNV')
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Tên', null=True, blank=True)
    cap = models.ForeignKey(HeSoLuong, on_delete=models.SET_NULL, verbose_name='Cấp bậc', null=True, blank=True)
    HD_CHOICE=[
        ('Toàn thời gian', 'Toàn thời gian'),
        ('Bán thời gian', 'Bán thời gian'),
        ('Thực tập sinh', 'Thực tập sinh')
    ]
    loaihd = models.CharField(max_length=20, choices = HD_CHOICE, verbose_name = 'Loại hợp đồng')
    sogio = models.FloatField(default=0.0, verbose_name='Số giờ làm việc', null=True, blank=True)
    luong = models.IntegerField(null=True, blank=True, verbose_name='Lương')
    THANG_CHOICE=[
        (1, 1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12),
    ]
    thang = models.IntegerField(choices=THANG_CHOICE, null=True, blank=True, verbose_name="Lương tháng")
    quyetdinh = models.ForeignKey(QuyetDinhLuong, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Quyết định tháng')
    chucvu = models.ForeignKey(ChucVu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Chức vụ')

    def save(self, *args, **kwargs):
        if self.thang:
            try:
                self.quyetdinh = QuyetDinhLuong.objects.get(month=self.thang)
            except:
                self.quyetdinh = QuyetDinhLuong.objects.filter().first()
        if self.cap:       
            if self.loaihd == 'Thực tập sinh':
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
                if self.loaihd == 'Toàn thời gian':
                    hsluong.manhour = hsluong.luongcoso / 26 / 8
                    self.luong = self.sogio * hsluong.manhour * hsluong.hsltheocap
                else: 
                    hsluong.manhour = hsluong.luongcoso / 26 / 8
                    self.luong = self.sogio * hsluong.manhour * hsluong.hsltheocap * self.quyetdinh.hesopt
                # print(self.luong)
                if self.chucvu:
                    self.luong += self.chucvu.thuong
            self.luong = int (round(self.luong, -4))
            # print(self.luong) 
        # if not self.cap and self.loaihd == 'Thực tập sinh':
        #     self.luong = 1200000

        
        super(NguoiLD, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Người Lao Động'


    def __str__(self):
        return str(self.mnv)
    
    def _cap(self):
        # qd = QuyetDinhTangBac.objects.filter(mnv = self.mnv, bac_moi = self.cap).first()
        # print(qd)
        try:
            qd = QuyetDinhTangBac.objects.filter(mnv = self, bac_moi = self.cap).first()
            # print(qd.date)
            # print(qd)
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
        # Tạo DataFrame từ dữ liệu lương
            data = {
                "Thông tin": ["Mã Nhân Viên", "Cấp", "Hệ số Lương theo cấp", 
                              "Lương cơ sở", "Loại hoạt động", 
                            "Số giờ làm việc", "Tổng lương", "Bằng chữ"],
                "Giá trị": [self.mnv, self.cap, self.cap.hsltheocap, 
                            self._luongcoso(), self.loaihd, 
                            self.sogio, self._luong(), self.luong_in_words()]
            }
            df = pd.DataFrame(data)

            # Vẽ bảng lương
            html_table = df.to_html(index=False, header=True, classes='table table-striped', border=2)

            return html_table
        except:
            return None
    bang_luong.short_description = 'Bảng Lương'


