from django.db import models

# Create your models here.

class ProcessData(models.Model):
    BATCH = (
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    )
    HALL = (
        (4, 'NLH'),
        (5, '204'),
        (6, '104'),
        (7, 'CIS Lab 1'),
        (8, 'CIS Lab 2'),
    )
    lecturer_name = models.CharField(max_length=100)
    batch = models.IntegerField(choices=BATCH)
    hall = models.IntegerField(choices=HALL)
    subject = models.CharField(max_length=50) 
    students = models.IntegerField()