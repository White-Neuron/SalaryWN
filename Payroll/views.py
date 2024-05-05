from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import NguoiLD
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render

def send_salary_email(request, nguoild_id):
    try:
        nguoild = NguoiLD.objects.get(id=nguoild_id)
        
        salary_table = nguoild.bang_luong()
        
        subject = 'Bảng lương'
        from_email = 'hostt4569@gmail.com'  
        to_email = [nguoild.email]

        html = render_to_string('email_template.html', {'salary_table': salary_table})

        send_mail(subject, '', from_email, to_email, html_message=html)
        
        
        messages.success(request, 'Email đã được gửi thành công')
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {str(e)}")

    return HttpResponseRedirect(reverse("admin:Payroll_nguoild_changelist"))
    # return HttpResponseRedirect(reverse("admin:index"))
    
# from ..ImportData.forms import ImportNguoiLDForm
# def import_nguoild(request):
#     print(request.method)
#     if request.method == 'POST':
#         form = ImportNguoiLDForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'File đã được import thành công')
#             return HttpResponseRedirect(reverse("admin:Payroll_nguoild_changelist"))
#     else:
#         form = ImportNguoiLDForm()
#     return render(request, 'admin/import_nguoild_form.html', {'form': form})

def splitnumber(number):
    array=[]
    number=str(number)
     #cắt thành 3 số 1 lần rồi thêm vào mảng
    while len(number)>3:
        array.append(number[-3:])
        number=number[:-3]
    array.append(number)
    return array
don_vi = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
chu_so_hang_chuc = ["linh", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi",
                    "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
hang_tram = ["", "trăm"]
don_vi_khoang= ["","nghìn","triệu","tỷ","nghìn tỷ","triệu tỷ","tỷ tỷ","nghìn tỷ tỷ","triệu tỷ tỷ","tỷ tỷ tỷ"]
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
# print(splitnumber(1234567809))
# print(read3digits('894'))
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
# print(readnumber(int(input("Nhập số: "))))

