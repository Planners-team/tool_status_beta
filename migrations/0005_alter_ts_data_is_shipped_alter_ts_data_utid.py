# Generated by Django 4.0.4 on 2022-08-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ts_system', '0004_ts_data_delete_ts_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ts_data',
            name='Is_SHIPPED',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='ts_data',
            name='UTID',
            field=models.CharField(max_length=250, primary_key=True, serialize=False),
        ),
    ]
