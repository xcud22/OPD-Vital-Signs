import uuid
from django.db import models
from patient.models import Person
from physician.models import Physician

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Person, on_delete=models.CASCADE)
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    reason_for_consultation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"