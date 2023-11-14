from django.db import models

class Physician(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    room_number = models.IntegerField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"