from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
# Create your views here.
# from .forms import ImportNguoiLDForm

def import_nguoild(request):
    print(request.method)
    if request.method == 'POST':
        form = ImportNguoiLDForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Lấy dữ liệu từ file Excel
            file = request.FILES['file']
            imported_data = pd.read_excel(file)
            
            for index, row in imported_data.iterrows():
                chucvu = ChucVu.objects.filter(kh=row[4]).first()
                print(chucvu)
                try: nguoild = NguoiLD.objects.get(
                        mnv=row[0], 
                        name=row[2],
                        email=row[3], 
                        chucvu=chucvu,
                        loaihd=row[9],
                    )
                except:
                    nguoild = NguoiLD(
                        mnv=row[0], 
                        name=row[2],
                        email=row[3], 
                        chucvu=chucvu,
                        loaihd=row[9],
                    )
                    nguoild.save()
            
            messages.success(request, 'File đã được import thành công')
            return HttpResponseRedirect(reverse("admin:Payroll_nguoild_changelist"))
    else:
        form = ImportNguoiLDForm()
    return render(request, 'admin/import_nguoild_form.html', {'form': form})


from datetime import datetime
def import_giolam(request):
    if request.method == 'POST':
        form = ImportGioLamForm(request.POST, request.FILES)
        tong = 0.0
        if form.is_valid():
            file = request.FILES['file']
            imported_data = pd.read_excel(file)
            for index, row in imported_data.iterrows():
                giolam = GioLam(
                    mnv = row[0],
                    date = row[1],
                    sogio = row[7],
                )
                giolam.save()
                
                nguoild = NguoiLD.objects.filter(mnv = giolam.mnv).first()
                luong_list = BangLuong.objects.filter(mnv=nguoild)
                time = datetime.strptime(str(giolam.sogio), '%H:%M:%S')
                hours = time.hour + time.minute / 60 + time.second / 3600
            
                for luong in luong_list:
                    # tong += hours
                    if not luong.month:
                        luong.month = giolam.thang
                    if luong.month == giolam.thang:
                        luong.sogio += round(hours, 2)
                        luong.save()
            messages.success(request, 'File đã được import thành công')
            return HttpResponseRedirect(reverse("admin:Payroll_giolam_changelist"))
    else:
        form = ImportGioLamForm()
    return render(request, 'admin/import_giolam_form.html', {'form': form})