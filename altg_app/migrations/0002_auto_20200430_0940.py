# Generated by Django 3.0.1 on 2020-04-30 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altg_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedschedules',
            name='schedule',
            field=models.CharField(max_length=500),
        ),
    ]
