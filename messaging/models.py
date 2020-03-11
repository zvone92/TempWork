from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):

      participants =  models.ManyToManyField(User)
      mesagges     =  models.ManyToManyField('Message')

class Message(models.Model):

    STATUS_CHOICES = {
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('archived', 'Archived')
    }

    message    = models.TextField()
    from_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    timestamp  = models.DateTimeField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')

    def correspondent(self, current_user):
        if self.from_user == current_user:
            return self.to_user
        else:
            return self.from_user

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
