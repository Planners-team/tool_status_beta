# Generated by Django 4.0.4 on 2022-09-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ts_system', '0025_argo_data_id_alter_argo_data_argo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ts_data',
            name='Voucher',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='ts_data',
            name='Open_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ts_data',
            name='Ship_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]