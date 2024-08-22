from django.db import models


class TelegramUser(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name} ({self.username})"
