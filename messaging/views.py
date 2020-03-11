from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import SendMessageForm



def messages(request, recipient_id=None):
    # CURRENT USER
    user = request.user

    #ALL CONVERSATIONS THAT USER IS PARTICIPATING IN
    recent_conversations = Conversation.objects.filter(participants=user).order_by('-pk')
    print('there are recent conversations',recent_conversations.exists())

    # IF THERE ARE NO RECENT CONVERSATIONS TO DISPLAY
    if not recent_conversations:
        # THERE WILL BE NO LAST MESSAGES TO DISPLAY FROM CONVERSATION
        last_message = None
    else:
        # LAST MESSAGE FROM EACH CONVERSATION
        last_message = [(i.mesagges.last(), i.mesagges.last().correspondent(user)) for i in recent_conversations]

    # CREATE FORM OBJECT IF MESSAGE FORM IS FILLED OUT
    form = SendMessageForm(request.POST or None)



    #IF NO RECIPIENT SELECTED, AND RECENT CONVERSATIONS EXISTS GET LAST CORRESPONDENT
    if (recipient_id  == None) and (recent_conversations.exists()):
        last_recipient =  Message.objects.last().correspondent(user)
        new_recipient = None
        last_conversation = recent_conversations.filter(participants=last_recipient).first()
        if last_conversation != None:
            #ALL MESSAGES FROM SELECTED CONVERSATION
            all_messages = last_conversation.mesagges.all()  # READ ALL MESSAGES
        # THERE ARE NO PREVIOUS CONVERSATION
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
            conversation.participants.add(user, last_recipient) # lst point
            # ADD MESSAGE TO BELONGING CONVERSATIONall_messages
            conversation.mesagges.add(message)

            return redirect('messages', last_recipient.id)

        else:
            last_conversation = recent_conversations.filter(participants=last_recipient).first()
            if  last_conversation != None:
                last_conversation.mesagges.add(message)
                new_recipient = None
            return redirect('messages', last_recipient.id)




    # RECIPIENT IS SELECTED AND CONVERSATIONS EXISTS
    elif (recipient_id != None) and (recent_conversations.exists()):
        last_conversation =  recent_conversations.filter(participants=recipient_id).first() # '.first' is used to return None if there is no last  conversation
        recipient = get_object_or_404(User, pk=recipient_id)  # CURRENT RECIPIENT
        new_recipient = recipient
        if last_conversation != None:
            #ALL MESSAGES FROM SELECTED CONVERSATION
            all_messages = last_conversation.mesagges.all()
            all_messages.filter(from_user=recipient, status='unread').update(status='read')  # READ ALL MESSAGES
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
                conversation.participants.add(user, recipient) # lst point
                # ADD MESSAGE TO BELONGING CONVERSATION
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


    #IF RECIPIENT IS SELECTED, AND THERE IS NO CONVERSATIONS
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
            conversation.participants.add(user, recipient) # lst point
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
