from django.db import models
from django.conf import settings

from accounts.models import Dialect

class Prompt(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text if len(self.text) <= 60 else self.text[:60] + "..."


class Submission(models.Model):

    class Status(models.TextChoices):
        PENDING = ("pending", "Pending")
        APPROVED = ("approved", "Approved")
        REJECTED = ("rejected", "Rejected")


    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="submissions")
    prompt = models.ForeignKey(Prompt, on_delete=models.PROTECT, related_name="submissions")
    audio = models.FileField(upload_to="submissions/%Y/%m/")
    transcription = models.TextField()
    dialect = models.CharField(max_length=20, choices=Dialect.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.pk} by {self.contributor}"


