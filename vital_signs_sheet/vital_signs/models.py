from django.db import models
from patient.models import Person
from transaction.models import Transaction

class VitalSigns(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    respiratory_rate = models.IntegerField()
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=10)
    oxygen_saturation = models.IntegerField()
    pain_scale = models.IntegerField()
    random_blood_sugar = models.FloatField()
    remarks = models.TextField()

    def save(self, *args, **kwargs):
        self.person = self.transaction.patient
        super().save(*args, **kwargs)