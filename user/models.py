from django.db import models
from django.contrib.auth.models import User

class UserAuthPassPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_images = models.TextField()
    auth_points = models.TextField()

    def __str__(self):
        return f"{self.user.username}"

class UserAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unauthorized_attempt_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"