# Generated by Django 5.0 on 2024-05-04 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ImportData', '0006_alter_importgiolam_sogio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importgiolam',
            name='date',
        ),
        migrations.RemoveField(
            model_name='importgiolam',
            name='mnv',
        ),
        migrations.RemoveField(
            model_name='importgiolam',
            name='quyetdinh',
        ),
        migrations.RemoveField(
            model_name='importgiolam',
            name='sogio',
        ),
        migrations.RemoveField(
            model_name='importgiolam',
            name='thang',
        ),
    ]
