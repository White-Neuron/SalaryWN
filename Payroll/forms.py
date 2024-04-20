from django import forms
from .models import *


class ImportNguoiLDForm(forms.ModelForm):
    file = forms.FileField(label='Chọn file Excel')

    class Meta:
        model = NguoiLD
        fields = ['file']