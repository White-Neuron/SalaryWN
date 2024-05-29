# Generated by Django 5.0 on 2024-04-20 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0017_alter_chucvu_thuong'),
    ]

    operations = [
        migrations.AddField(
            model_name='nguoild',
            name='chucvu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Payroll.chucvu', verbose_name='Chức vụ'),
        ),
    ]
