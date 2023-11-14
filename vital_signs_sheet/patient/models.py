from django.db import models
from datetime import date

class Person(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
