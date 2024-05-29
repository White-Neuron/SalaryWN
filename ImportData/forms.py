from django import forms
from Payroll.models import *
from .models import *


class ImportNguoiLDForm(forms.ModelForm):
    file = forms.FileField(label='Chọn file Excel')

    class Meta:
        model = NguoiLD
        fields = ['file'] 


class ImportGioLamForm(forms.ModelForm):
    file = forms.FileField(label='Chọn file Excel')

    class Meta:
        model = ImportGio
        fields = ['file']


