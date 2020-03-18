from .models import Message
from django.contrib.auth.models import User


def new_messages(current_user):
    '''
    counting all message objects that are sent to current user,
    and that have status field 'unread'
    '''
    new_msg_count = Message.objects.filter(to_user=current_user, status='unread').count()
    return new_msg_count # returns number of unread messages
