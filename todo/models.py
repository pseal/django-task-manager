from django.db import models
from django.contrib.auth.models import User # <-- Import Django's built-in User model

class Task(models.Model):
    # This creates an SQL Foreign Key linking the task to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
