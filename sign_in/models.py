from django.db import models
from django.utils import timezone
from users.models import CustomUser

class SignInRecord(models.Model):
    student = models.ForeignKey('StudentReference', on_delete=models.SET_NULL, null=True, blank=True)

    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=50)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def formatted_reason(self):
        return self.reason.replace("_", " ").capitalize() # Returns a reason that looks nice (uppercase, no underscores)

    def is_signed_out(self):
        return self.time_out is not None

    def duration(self):
        if self.time_out:
            return self.time_out - self.time_in
        return timezone.now() - self.time_in
    
# sign_in/models.py

class StudentReference(models.Model):
    student_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student_id} – {self.first_name} {self.last_name}"