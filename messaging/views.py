from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SendMessageForm


@login_required
def messages(request, recipient_id=None):
    # current user
    user = request.user

    # all conversations that current user is participating
    recent_conversations = Conversation.objects.filter(participants=user).order_by('-pk')

    # if there are no recent conversations to display
    if not recent_conversations:
        # there will be no last messages to display from conversation
        last_message = None
    else:
        # last message from each conversation
        last_message = [(i.mesagges.last(), i.mesagges.last().correspondent(user)) for i in recent_conversations]

    # create form object if message form is filled out
    form = SendMessageForm(request.POST or None)

    # if no recipient is selected, and recent conversations exists: get the last correspondent
    if (recipient_id  == None) and (recent_conversations.exists()):
        last_recipient =  Message.objects.last().correspondent(user)
        new_recipient = None
        last_conversation = recent_conversations.filter(participants=last_recipient).first()
        if last_conversation != None:
            # all messages from selected conversation
            all_messages = last_conversation.mesagges.all()  # READ ALL MESSAGES
        # there are no previous conversation
        else:
            all_messages= None

        context = {'recent_conversations':last_message,
                   'last_conversation': all_messages,
                   'form': form,
                   'new_recipient': new_recipient
                   }

        if form.is_valid():
            message = form.save(commit=False)
            message.from_user  =  user
            message.to_user    =  last_recipient
            message.timestamp  = timezone.datetime.now()
            message.save()
        else:
            return render(request, 'messaging/messages.html', context)

        if recent_conversations.filter(participants=last_recipient).exists() != True:
            new_recipient = last_recipient
            conversation = Conversation.objects.create()
            conversation.save()
            conversation.participants.add(user, last_recipient)
            # add message to belonging conversation
            conversation.mesagges.add(message)

            return redirect('messages', last_recipient.id)

        else:
            last_conversation = recent_conversations.filter(participants=last_recipient).first()
            if  last_conversation != None:
                last_conversation.mesagges.add(message)
                new_recipient = None
            return redirect('messages', last_recipient.id)


    # recipient is selected and conversations exists
    elif (recipient_id != None) and (recent_conversations.exists()):
        last_conversation =  recent_conversations.filter(participants=recipient_id).first() # '.first' is used to return None if there is no last  conversation
        recipient = get_object_or_404(User, pk=recipient_id)  # CURRENT RECIPIENT
        new_recipient = recipient
        if last_conversation != None:
            # all messages from selected conversation
            all_messages = last_conversation.mesagges.all()
            # change unread message status to 'read'
            all_messages.filter(from_user=recipient, status='unread').update(status='read')
            for msg in all_messages:
                msg.save()
        else:
            all_messages= None

        context = {'recent_conversations':last_message,
                   'last_conversation': all_messages,
                   'form': form,
                   'new_recipient': new_recipient
                   }

        if form.is_valid():
            message = form.save(commit=False)
            message.from_user  =  user
            message.to_user    =  recipient
            message.timestamp  = timezone.datetime.now()
            message.save()

            if recent_conversations.filter(participants=recipient).exists() != True:
                new_recipient = recipient
                conversation = Conversation.objects.create()
                conversation.save()
                conversation.participants.add(user, recipient)
                # add message to belonging conversation
                conversation.mesagges.add(message)
                new_recipient = recipient
                return redirect('messages', recipient.id)

            else:
                last_conversation = recent_conversations.filter(participants=recipient_id).first()
                if  last_conversation != None:
                    last_conversation.mesagges.add(message)
                    new_recipient = recipient
            new_recipient = recipient
            return redirect('messages', recipient.id)

        new_recipient = recipient
        return render(request, 'messaging/messages.html', context)


    # if recipient is selected, and there is no conversations
    elif (recipient_id  != None) and (recent_conversations.exists() != True):
        recipient = get_object_or_404(User, pk=recipient_id)
        new_recipient = recipient
        last_conversation =  None
        all_messages= None

        context = {'recent_conversations':last_message,
                   'last_conversation': all_messages,
                   'form': form,
                   'new_recipient': new_recipient
                   }

        if form.is_valid():
            message = form.save(commit=False)
            message.from_user  =  user
            message.to_user    =  recipient
            message.timestamp  = timezone.datetime.now()
            message.save()

            conversation = Conversation.objects.create()
            conversation.save()
            conversation.participants.add(user, recipient)
            conversation.mesagges.add(message)


        else:
            return render(request, 'messaging/messages.html', context)


        return redirect('messages', recipient.id)

    else:
        new_recipient = None
        last_message = None
        all_messages = None


    context = {'recent_conversations':last_message,
               'last_conversation': all_messages,
               'form': form,
               'new_recipient': new_recipient
               }

    return render(request, 'messaging/messages.html', context)
