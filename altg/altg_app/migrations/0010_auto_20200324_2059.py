# Generated by Django 3.0.1 on 2020-03-24 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altg_app', '0009_delete_lecturehalls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_profile',
            field=models.ImageField(upload_to='user/'),
        ),
    ]
