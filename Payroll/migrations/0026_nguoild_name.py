# Generated by Django 5.0 on 2024-04-22 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0025_alter_nguoild_loaihd'),
    ]

    operations = [
        migrations.AddField(
            model_name='nguoild',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tên'),
        ),
    ]
