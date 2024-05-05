# Generated by Django 5.0 on 2024-05-04 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0033_alter_nguoild_quyetdinh_alter_capbac_qd_and_more'),
        ('QuyetDinh', '0002_rename_quyetdinh_quyetdinhluong_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuyetDinhTangBac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Ngày quyết định')),
                ('bac_cu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Payroll.hesoluong', verbose_name='Bậc cũ')),
            ],
        ),
    ]