from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    STATUS_CHOICES = {
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('archived', 'Archived')
    }

    message    = models.CharField(max_length=125)
    from_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    timestamp  = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')


    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
