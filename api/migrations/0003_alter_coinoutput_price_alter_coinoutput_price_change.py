# Generated by Django 5.0.6 on 2024-06-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinoutput',
            name='price',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='coinoutput',
            name='price_change',
            field=models.CharField(max_length=10),
        ),
    ]