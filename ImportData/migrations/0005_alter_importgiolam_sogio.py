# Generated by Django 5.0 on 2024-05-04 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImportData', '0004_importgiolam_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importgiolam',
            name='sogio',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Số giờ làm việc'),
        ),
    ]
