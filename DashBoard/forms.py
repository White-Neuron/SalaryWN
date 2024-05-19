from django import forms
from Payroll.models import *
from .models import *


class SelectEmpForm(forms.ModelForm):
    employee_id = forms.ModelChoiceField(queryset=NguoiLD.objects.all(), label='Chọn mã nhân viên')

    class Meta:
        model = NguoiLD
        fields = ['employee_id'] 