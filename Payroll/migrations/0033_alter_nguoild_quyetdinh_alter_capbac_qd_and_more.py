# Generated by Django 5.0 on 2024-05-04 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0032_giolam'),
        ('QuyetDinh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoild',
            name='quyetdinh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuyetDinh.quyetdinh', verbose_name='Quyết định tháng'),
        ),
        migrations.AlterField(
            model_name='capbac',
            name='qd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.quyetdinh', verbose_name='Quyết định'),
        ),
        migrations.AlterField(
            model_name='hesoluong',
            name='qd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.quyetdinh', verbose_name='Quyết định'),
        ),
        migrations.AlterField(
            model_name='giolam',
            name='quyetdinh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuyetDinh.quyetdinh', verbose_name='Quyết định tháng'),
        ),
        migrations.AlterField(
            model_name='chucvu',
            name='qd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuyetDinh.quyetdinh', verbose_name='Quyết định'),
        ),
        migrations.DeleteModel(
            name='QuyetDinh',
        ),
    ]