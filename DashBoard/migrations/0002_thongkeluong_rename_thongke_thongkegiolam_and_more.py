# Generated by Django 5.0 on 2024-05-13 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashBoard', '0001_initial'),
        ('Payroll', '0041_merge_20240509_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThongKeLuong',
            fields=[
                ('bangluong_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Payroll.bangluong')),
            ],
            options={
                'verbose_name_plural': 'Thống Kê Lương',
            },
            bases=('Payroll.bangluong',),
        ),
        migrations.RenameModel(
            old_name='ThongKe',
            new_name='ThongKeGioLam',
        ),
        migrations.AlterModelOptions(
            name='thongkegiolam',
            options={'verbose_name_plural': 'Thống Kê Giờ Làm'},
        ),
    ]