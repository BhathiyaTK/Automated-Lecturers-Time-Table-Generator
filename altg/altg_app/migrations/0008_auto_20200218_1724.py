# Generated by Django 3.0.1 on 2020-02-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altg_app', '0007_auto_20200215_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturers',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('guest', 'Guest')], max_length=20),
        ),
    ]
