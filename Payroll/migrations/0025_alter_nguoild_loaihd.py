# Generated by Django 5.0 on 2024-04-22 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0024_alter_chucvu_kh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoild',
            name='loaihd',
            field=models.CharField(choices=[('Toàn thời gian', 'Toàn thời gian'), ('Bán thời gian', 'Bán thời gian'), ('Thực tập sinh', 'Thực tập sinh')], max_length=20, verbose_name='Loại hợp đồng'),
        ),
    ]
