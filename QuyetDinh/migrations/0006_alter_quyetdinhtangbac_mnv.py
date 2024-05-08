# Generated by Django 4.2.7 on 2024-05-06 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll', '0037_alter_bangluong_mnv'),
        ('QuyetDinh', '0005_alter_quyetdinhtangbac_options_quyetdinhtangbac_mnv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quyetdinhtangbac',
            name='mnv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Payroll.nguoild', verbose_name='Mã nhân viên'),
        ),
    ]