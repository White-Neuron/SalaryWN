# Generated by Django 5.0 on 2024-05-09 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ImportData', '0008_rename_importgiolam_importgio_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importgio',
            options={'verbose_name': 'Nhập dữ liệu Giờ Làm', 'verbose_name_plural': 'Nhập dữ liệu Giờ Làm'},
        ),
        migrations.AlterModelOptions(
            name='importnhanvien',
            options={'verbose_name': 'Nhập dữ liệu Người Lao Động', 'verbose_name_plural': 'Nhập dữ liệu Người Lao Động'},
        ),
    ]