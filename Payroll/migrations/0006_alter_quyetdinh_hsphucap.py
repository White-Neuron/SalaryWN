# Generated by Django 5.0 on 2024-03-22 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0005_quyetdinh_bhyt_quyetdinh_hsdieuchinh_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quyetdinh',
            name='hsphucap',
            field=models.FloatField(default=0, verbose_name='Hệ số phụ cấp'),
        ),
    ]
