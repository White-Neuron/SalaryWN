# Generated by Django 5.0 on 2024-04-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0021_alter_quyetdinh_sogio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quyetdinh',
            name='sogio',
            field=models.FloatField(verbose_name='Giờ làm việc một ngày'),
        ),
    ]
