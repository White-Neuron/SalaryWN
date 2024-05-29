# Generated by Django 5.0 on 2024-03-21 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeSoLuong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cap', models.CharField(blank=True, max_length=20, null=True, verbose_name='Cấp bậc')),
                ('hsltheocap', models.FloatField(blank=True, null=True, verbose_name='Hệ số lương theo cấp bậc')),
                ('hsphucap', models.FloatField(default=0.0, verbose_name='Hệ số phụ cấp')),
                ('luongcoso', models.IntegerField(default=1800000, verbose_name='Lương cơ sở')),
                ('hsdieuchinh', models.FloatField(default=0.9, verbose_name='Hệ số điều chỉnh')),
                ('bhyt', models.FloatField(default=0.235, verbose_name='Bảo hiểm y tế')),
                ('giangaycong', models.IntegerField(blank=True, null=True, verbose_name='Giá một ngày công')),
            ],
            options={
                'verbose_name_plural': 'Hệ Số Lương',
            },
        ),
        migrations.CreateModel(
            name='QuyetDinh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Ngày ban hành')),
                ('month', models.IntegerField(blank=True, null=True, verbose_name='Quyết định tháng')),
                ('hesopt', models.FloatField(default=0.8, verbose_name='Hệ số part time')),
            ],
            options={
                'verbose_name_plural': 'Quyết Định',
            },
        ),
        migrations.AlterModelOptions(
            name='capbac',
            options={'verbose_name_plural': 'Cấp Bậc'},
        ),
        migrations.RemoveField(
            model_name='capbac',
            name='des',
        ),
        migrations.AddField(
            model_name='capbac',
            name='cb',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Ký hiệu'),
        ),
        migrations.AlterField(
            model_name='capbac',
            name='heso',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tổng Bậc'),
        ),
        migrations.AlterField(
            model_name='capbac',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Tên'),
        ),
        migrations.CreateModel(
            name='NguoiLD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mnv', models.IntegerField(verbose_name='MNV')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('loaihd', models.CharField(choices=[('F', 'Full Time'), ('P', 'Part Time')], max_length=20, verbose_name='Loại hợp đồng')),
                ('songay', models.IntegerField(verbose_name='Số ngày đi làm')),
                ('luong', models.IntegerField(blank=True, null=True, verbose_name='Lương')),
                ('thang', models.DateField(blank=True, null=True, verbose_name='Tháng')),
                ('cap', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Payroll.hesoluong', verbose_name='Cấp')),
                ('quyetdinh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Payroll.quyetdinh', verbose_name='Quyết định tháng')),
            ],
            options={
                'verbose_name_plural': 'Người Lao Động',
            },
        ),
        migrations.AddField(
            model_name='hesoluong',
            name='qd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Payroll.quyetdinh', verbose_name='Quyết định'),
        ),
        migrations.AddField(
            model_name='capbac',
            name='qd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Payroll.quyetdinh', verbose_name='Quyết định'),
        ),
    ]
