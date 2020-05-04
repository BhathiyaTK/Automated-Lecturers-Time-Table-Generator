# Generated by Django 3.0.1 on 2020-03-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altg_app', '0003_remove_subjects_extra_column'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=100)),
                ('subject_name', models.CharField(max_length=224)),
                ('related_batch', models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')], default=None, max_length=20)),
                ('related_lecturer', models.CharField(default='', max_length=224)),
            ],
        ),
    ]