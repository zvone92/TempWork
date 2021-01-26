from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Conversation, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SendMessageForm
from django.core.exceptions import ObjectDoesNotExist


@login_required
def conversation_list(request):
    # current user
    user = request.user
    query   = request.GET.get('q')

    # all conversations that current user is participating, starting from last one
    recent_conversations = Conversation.objects.filter(participants=user).order_by('-pk')

    # if there is a search query, find by user
    if query:
        correspondent = User.objects.filter(username__icontains=query).exclude(username=user.username)
        recent_conversations = recent_conversations.filter(participants__in=correspondent)
            #return redirect('conversation_list')

    # if there are no recent conversations to display
    if not recent_conversations:
        # there will be no last messages to display from conversation
        last_messages = None
    else:
        # get last message from each conversation
        last_messages = []
        for conversation in recent_conversations:
            message = conversation.mesagges.last()
            if message != None:
                correspondent = conversation.mesagges.last().correspondent(user)
            else:
                continue

            last_messages.append((message, correspondent))

        # last_message = [(i.mesagges.last(), i.mesagges.last().correspondent(user)) for i in recent_conversations]

    context = {'recent_conversations': last_messages}

    return render(request, 'messaging/conversation-list.html', context)



@login_required
def message_box(request, recipient_id=None):
    # current user
    user = request.user
    # recipient
    recipient = get_object_or_404(User, pk=recipient_id)

    all_user_conversations = Conversation.objects.filter(participants=user).order_by('-pk')
    # Check if there is existing conversation between this user and other user (recipient)
    conversation_with_recipient =  all_user_conversations.filter(participants=recipient_id).first() # '.first' is used to return None if there is no conversation

    # if conversation exists
    if conversation_with_recipient != None:
        # all messages from selected conversation
        all_messages = conversation_with_recipient.mesagges.order_by('pk')
        # change unread message status to 'read'
        all_messages.filter(from_user=recipient, status='unread').update(status='read')
        for msg in all_messages:
            msg.save()
    else:
        all_messages= None

    # create form object if message form is filled out
    form = SendMessageForm(request.POST or None)

    context = {'last_conversation': all_messages,
               'form': form,
               'recipient': recipient,
               }

    # if message is sent
    if form.is_valid():
        message = form.save(commit=False)
        message.from_user  =  user
        message.to_user    =  recipient
        message.timestamp  = timezone.datetime.now()
        message.save()

        # if there is no previous conversation with this user
        if all_user_conversations.filter(participants=recipient).exists() != True:
            # create conversation
            conversation = Conversation.objects.create()
            conversation.save()
            conversation.participants.add(user, recipient)
            # add message to belonging conversation
            conversation.mesagges.add(message)
            new_recipient = recipient
            return redirect('message_box', recipient.id)
        # find conversation and add message to it
        else:
            last_conversation = all_user_conversations.filter(participants=recipient_id).first()
            if  last_conversation != None:
                last_conversation.mesagges.add(message)

        # refresh page
        return redirect('message_box', recipient.id)

    return render(request, 'messaging/message-box.html', context)
