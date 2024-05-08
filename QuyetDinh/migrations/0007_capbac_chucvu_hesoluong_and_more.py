# Generated by Django 5.0 on 2024-05-07 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuyetDinh', '0006_alter_quyetdinhtangbac_mnv'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapBac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cb', models.CharField(blank=True, max_length=20, null=True, verbose_name='Ký hiệu')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tên')),
                ('heso', models.IntegerField(blank=True, null=True, verbose_name='Tổng Bậc')),
                ('qd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.quyetdinhluong', verbose_name='Quyết định')),
            ],
            options={
                'verbose_name_plural': 'Cấp Bậc',
            },
        ),
        migrations.CreateModel(
            name='ChucVu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kh', models.CharField(blank=True, max_length=20, null=True, verbose_name='Ký hiệu')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tên')),
                ('thuong', models.IntegerField(blank=True, null=True, verbose_name='Thưởng phụ cấp')),
                ('qd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.quyetdinhluong', verbose_name='Quyết định')),
            ],
            options={
                'verbose_name_plural': 'Chức Vụ',
            },
        ),
        migrations.CreateModel(
            name='HeSoLuong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bac', models.IntegerField(blank=True, null=True, verbose_name='Bậc')),
                ('hsltheocap', models.FloatField(blank=True, default=1.0, null=True, verbose_name='Hệ số lương theo cấp bậc')),
                ('muctang', models.FloatField(blank=True, null=True, verbose_name='Mức tăng')),
                ('luongcoso', models.IntegerField(blank=True, null=True, verbose_name='Lương cơ sở')),
                ('manhour', models.IntegerField(blank=True, null=True, verbose_name='Lương cơ sở theo giờ')),
                ('loaibac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.capbac', verbose_name='Loại bậc')),
                ('qd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.quyetdinhluong', verbose_name='Quyết định')),
            ],
            options={
                'verbose_name_plural': 'Hệ Số Lương',
            },
        ),
        migrations.AlterField(
            model_name='quyetdinhtangbac',
            name='bac_cu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bac_cu_quyetdinh_set', to='QuyetDinh.hesoluong', verbose_name='Bậc cũ'),
        ),
        migrations.AlterField(
            model_name='quyetdinhtangbac',
            name='bac_moi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bac_moi_quyetdinh_set', to='QuyetDinh.hesoluong', verbose_name='Bậc mới'),
        ),
    ]