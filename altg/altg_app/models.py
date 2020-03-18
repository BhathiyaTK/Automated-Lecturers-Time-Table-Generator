from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('guest', 'Guest'),
    )
    first_name = models.CharField(max_length=224, default=None)
    last_name = models.CharField(max_length=224, default=None)
    lecturer_name = models.CharField(max_length=224, default=None)
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    lecturer_code = models.CharField(max_length=224)
    user_profile = models.ImageField(upload_to='media/')

class ProcessData(models.Model):
    BATCH = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    )  
    HALL = (
        ('NLH', 'NLH'),
        ('204', '204'),
        ('104', '104'),
        ('cis1', 'CIS Lab 1'),
        ('cis2', 'CIS Lab 2'),
    )
    lecturer_name = models.CharField(max_length=100)
    batch = models.IntegerField(choices=BATCH)
    hall = models.IntegerField(choices=HALL)
    subject = models.CharField(max_length=50) 
    students = models.IntegerField()

class LectureHalls(models.Model):
    hall_number = models.CharField(max_length=224)
    hall_name = models.CharField(max_length=224)

class Subjects(models.Model):
    BATCH = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    )
    subject_code = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=224)
    related_batch = models.IntegerField(choices=BATCH)
    related_lecturer = models.CharField(max_length=224, default='')

class Batch(models.Model):
    batch_no = models.CharField(max_length=50)
    no_of_students = models.CharField(max_length=100)

class TimeSlots(models.Model):
    time_slot = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)

class Days(models.Model):
    days = models.CharField(max_length=150)
    batch = models.CharField(max_length=50)