from django.db import models

class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    phone = models.CharField(max_length=20)
    preferred_datetime = models.DateTimeField(verbose_name="Preferred Date and Time")
    reason = models.TextField()

    def __str__(self):
        return f"{self.full_name} - {self.preferred_datetime}"