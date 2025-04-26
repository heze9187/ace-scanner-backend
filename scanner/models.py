# scanner/models.py
from django.db import models
from django.contrib.auth.models import User

class Court(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class CourtAvailability(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)  # Example: "7:00 PM"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.court.name} - {self.date} {self.time}"

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    weekday_start = models.IntegerField(default=1700)
    weekday_end = models.IntegerField(default=2400)
    weekend_start = models.IntegerField(default=900)
    weekend_end = models.IntegerField(default=2400)
    receive_email = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} preference for {self.court.name}"