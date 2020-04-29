from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from PIL import Image

class User(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('guest', 'Guest'),
    )
    TITLES = (
        ('Prof', 'Prof'),
        ('Dr', 'Dr'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
    )
    POSITION = (
        ('lecturer', 'Lecturer'),
        ('demo', 'Demonstrator'),
        ('naStaff', 'Non Acedamic Staff'),
        ('other', 'Other'),
    )
    user_title = models.CharField(max_length=30, choices=TITLES, default=None)
    first_name = models.CharField(max_length=224, default=None)
    last_name = models.CharField(max_length=224, default=None)
    lecturer_name = models.CharField(max_length=224, default=None)
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    lecturer_code = models.CharField(max_length=224)
    user_position = models.CharField(max_length=30, choices=POSITION, default=None)

    def get_profile_img(self):
        try:
            return Profiles.objects.filter(username=self.username).values_list('user_profile_img', flat=True)[0]
        except:
            return None

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

class AllLectureHalls(models.Model):
    hall_number = models.CharField(max_length=224)
    hall_name = models.CharField(max_length=224)
    hall_capacity = models.IntegerField()

class AllSubjects(models.Model):
    BATCH = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    )
    SEMESTERS = (
        ('1', 'Semester I'),
        ('2', 'Semester II'),
    )
    subject_code = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=224)
    related_batch = models.CharField(max_length=20, choices=BATCH, default=None)
    semester = models.CharField(max_length=20, choices=SEMESTERS, default=None)
    related_lecturer = models.CharField(max_length=224, default='')
    std_count = models.IntegerField()

class AllBatches(models.Model):
    batch_no = models.CharField(max_length=20)
    batch_name_suffix = models.CharField(max_length=20)
    no_of_students = models.CharField(max_length=50)

class AllSemesters(models.Model):
    semester_no = models.CharField(max_length=20)
    semester_name_suffix = models.CharField(max_length=20)

class AllTimeSlots(models.Model):
    slot_id = models.CharField(max_length=50)
    time_slot = models.CharField(max_length=100)

class Profiles(models.Model):
    username = models.CharField(max_length=224)
    user_profile_img = models.ImageField(upload_to='users/', blank=True, null=True)

    def save(self):
        super().save()
        img = Image.open(self.user_profile_img.path)
        if img.height > img.width:
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2

            img = img.crop((left, top, right, bottom))

        elif img.width > img.height:
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height

            img = img.crop((left, top, right, bottom))

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_profile_img.path)
