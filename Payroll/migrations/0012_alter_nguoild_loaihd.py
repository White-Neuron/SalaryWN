# Generated by Django 5.0 on 2024-03-25 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0011_hesoluong_bac_hesoluong_loaibac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoild',
            name='loaihd',
            field=models.CharField(choices=[('Toàn thời gian', 'Toàn thời gian'), ('Bán thời gian', 'Bán thời gian')], max_length=20, verbose_name='Loại hợp đồng'),
        ),
    ]
