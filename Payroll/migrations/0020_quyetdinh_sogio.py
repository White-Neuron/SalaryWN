# Generated by Django 5.0 on 2024-04-20 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0019_remove_nguoild_songay_hesoluong_giagiocong_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quyetdinh',
            name='sogio',
            field=models.IntegerField(default=8, verbose_name='Giờ làm việc một ngày'),
        ),
    ]
