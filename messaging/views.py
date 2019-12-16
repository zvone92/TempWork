from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import SendMessageForm





def messages(request, user_id=None):

    recent_people     = Message.objects.filter(Q(from_user=request.user) | Q(to_user=request.user)).distinct('from_user').exclude(from_user=request.user)

    last_conversation = Message.objects.filter(Q(from_user=request.user, to_user=user_id) | Q(to_user=request.user, from_user=user_id))   #, Q(to_user=request.user) | Q(from_user=user_id)

    form = SendMessageForm(request.POST or None)

    context = {'recent_people': recent_people,
               'last_conversation': last_conversation,
               'form': form
    }

    if user_id != None:
        recipient = User.objects.get(pk=user_id)
        if form.is_valid():
            message = form.save(commit=False)   # commit=False tells Django not to send this to database yet, until i make some changes to it.
            message.from_user  = request.user
            message.to_user  =   recipient
            message.save() # Now save it to database

        else:
            return render(request, 'messaging/messages.html', context)


    return render(request, 'messaging/messages.html', context)
