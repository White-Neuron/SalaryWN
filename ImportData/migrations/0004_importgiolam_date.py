# Generated by Django 5.0 on 2024-05-03 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImportData', '0003_importgiolam_mnv_importgiolam_sogio'),
    ]

    operations = [
        migrations.AddField(
            model_name='importgiolam',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Ngày làm việc'),
        ),
    ]