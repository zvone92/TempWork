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

    message    = models.CharField(max_length=125)
    from_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    timestamp  = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    #!! If you decide to accept 'new_field' as a nullable field you may want to accept 'no input' as valid input . Then you have to add the blank=True statement as well:
    #conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, blank=True, null=True)
    def correspondent(self, current_user):
        if self.from_user == current_user:
            return self.to_user
        else:
            return self.from_user

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
