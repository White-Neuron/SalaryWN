from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import NguoiLD
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render
from django.core.exceptions import ValidationError
def send_salary_email(request, nguoild_id):
    try:
        nguoild = NguoiLD.objects.get(id=nguoild_id)
        print(nguoild.luong)
        if nguoild.luong is None:
            raise ValidationError("Người lao động chưa có lương")
        else:
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
    
