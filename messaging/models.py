from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    '''
        this model represents a conversation between
        two or more participants exchanging text messages
        with each other.
    '''
    participants =  models.ManyToManyField(User)
    mesagges     =  models.ManyToManyField('Message')

class Message(models.Model):
    '''
        this model represents a text message that
        can be sent to user and received from user.
    '''

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
        '''
            this method is used to distinguish the current user from the participants
            in the conversation, and thus in previous conversations show the person
            with whom we are exchanging messages and not the current user.
        '''
        if self.from_user == current_user:
            return self.to_user
        else:
            return self.from_user

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
