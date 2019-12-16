from .models import Message
from django.contrib.auth.models import User


def new_messages(current_user):
    new_msg_count = Message.objects.filter(to_user=current_user, status='unread').count()
    return new_msg_count
