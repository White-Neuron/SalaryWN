# Generated by Django 5.0 on 2024-04-22 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImportData', '0002_importgiolam_quyetdinh_importgiolam_thang'),
    ]

    operations = [
        migrations.AddField(
            model_name='importgiolam',
            name='mnv',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='MNV'),
        ),
        migrations.AddField(
            model_name='importgiolam',
            name='sogio',
            field=models.TimeField(blank=True, null=True, verbose_name='Số giờ làm việc'),
        ),
    ]
