# Generated by Django 4.2.7 on 2024-05-06 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QuyetDinh', '0005_alter_quyetdinhtangbac_options_quyetdinhtangbac_mnv'),
        ('Payroll', '0034_alter_nguoild_cap'),
    ]

    operations = [
        migrations.CreateModel(
            name='BangLuong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], null=True, verbose_name='Lương tháng')),
                ('mnv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Payroll.nguoild', verbose_name='Mã nhân viên')),
                ('qdbac', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuyetDinh.quyetdinhtangbac', verbose_name='Quyết định tăng bậc')),
                ('qdluong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuyetDinh.quyetdinhluong', verbose_name='Quyết định lương')),
            ],
            options={
                'verbose_name_plural': 'Người Lao Động',
            },
        ),
    ]
