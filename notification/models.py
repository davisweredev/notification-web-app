from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reciever = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="notifications"
    )
    sender = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="sent_notifications"
    )


    def __str__(self):
        return f"Notification to {self.user.username}: {self.message[:20]}"
