# Generated by Django 5.0 on 2024-05-20 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0041_merge_20240509_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='bangluong',
            name='canhbao',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cảnh báo'),
        ),
    ]