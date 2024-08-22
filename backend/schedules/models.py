from django.db import models
from telegram_users.models import TelegramUser


class Schedule(models.Model):
    users = models.ManyToManyField(TelegramUser, related_name="schedules")
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "date",
                ],
                name="date",
            )
        ]

    def users_count(self):
        return self.users.count()

    def __str__(self):
        return f"{self.date} - {self.users_count()} игрок(а)"
