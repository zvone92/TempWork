from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import SendMessageForm


def messages(request, recipient_id=None):
    # CURRENT USER
    user = request.user
    # IF NO RECIPIENT SELECTED, GET LAST CORRESPONDENT
    if recipient_id  == None:
        last_recipient =  Message.objects.last().correspondent(user) # BUG IF NO MESSGS!

    #ALL CONVERSATIONS THAT USER IS PARTICIPATING IN
    recent_conversations = Conversation.objects.filter(participants=user)
    print(recent_conversations)
    # LAST MESSAGE FROM EACH CONVERSATION
    last_message = [(i.mesagges.last(), i.mesagges.last().correspondent(user)) for i in recent_conversations]


    # IF THERE IS NO RECIPIENT SELECTED, GET THE LAST CONVERSATION
    if recipient_id == None:
        last_conversation = recent_conversations.filter(participants=last_recipient).first() # need to be from last msg sent conversation
        # IF PREVIOUS CONVERSATION EXISTS
        if last_conversation != None:
            #ALL MESSAGES FROM SELECTED CONVERSATION
            all_messages = last_conversation.mesagges.all()
        # THERE ARE NO PREVIOUS CONVERSATION
        else:
            all_messages= None

    # IF RECIPIENT SELECTED, GET CONVERSATION WITH THIS RECIPIENT
    else:
        last_conversation =  recent_conversations.filter(participants=recipient_id).first() #change from first()
        if last_conversation != None:
            #ALL MESSAGES FROM SELECTED CONVERSATION
            all_messages= last_conversation.mesagges.all()
            last_recipient = all_messages.last().correspondent(user)
        else:
            all_messages= None

    # CREATE FORM OBJECT IF MESSAGE FORM IS FILLED OUT
    form = SendMessageForm(request.POST or None)

    context = {'recent_conversations':last_message,
               'last_conversation': all_messages,
               'form': form,
               }

    # IF USER ENTERED CONVERSATION WITH RECIPIENT
    if last_recipient != None:
        # 'READ' ALL 'UNREAD' MESSAGES FROM THAT CONVERSATION
        if all_messages != None:
            for message in all_messages:
                if (message.status == 'unread') and (message.from_user != user):
                    message.status = 'read'
                    message.save()
        # RECIPIENT
        recipient = last_recipient
        #User.objects.get(pk=recipient_id)
        # IF USER SENT VALID MESSAGE, SAVE THAT MESSAGE
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user  =  user
            message.to_user    =  recipient
            message.save()
            # CREATE CONVERSATION WITH THIS PERSON, IF IT DOESN'T EXISTS
            if recent_conversations.filter(participants=recipient).exists() != True: # bug:
                #recipient = get_object_or_404(User, pk=recipient_id)
                conversation = Conversation.objects.create()
                conversation.save()
                conversation.participants.add(user, recipient) # lst point
            # ADD MESSAGE TO BELONGING CONVERSATION
            last_conversation = recent_conversations.filter(participants=recipient).first()
            if  last_conversation != None:
                last_conversation.mesagges.add(message)
            return redirect('messages', recipient.id)
        #render the same page with empty form
        else:
            print("here first")
            return render(request, 'messaging/messages.html', context)
    print("here second")
    return render(request, 'messaging/messages.html', context)



'''

def messages(request, user_id=None):

    Displays messages page showing all people that user have previously exchanged messages with, also if there is user_id(recipient) selected,
    all exchanged messages beetwen that recepient and user will be displayed. It also displays a message form to be filled, and if message form is filled and sent
    it will save message object with recipient(user_id) as message recepient.

    sender    = request.user
    #recent_people     = Message.objects.filter(Q(from_user=request.user) | Q(to_user=request.user)).distinct('from_user')#.distinct('to_user')#.exclude(from_user=request.user)#.order_by('from_user', '-timestamp')
    #recent_people = Message.objects.filter(Q(from_user=request.user)).distinct('from_user')#.exclude(from_user=request.user).order_by('from_user', '-timestamp')

    #all users that have been previously exchanging messages with user requesting the page (request.user)
    recent_people = Message.objects.filter(conversation__participants__in=[request.user]).distinct('to_user')#(Q(conversation__participants=sender) & Q(conversation__participants=user_id))

    #all messages that have been exchanged beetwen this user and selected recipient(user_id)
    last_conversation = Message.objects.filter(Q(from_user=request.user, to_user=user_id) | Q(to_user=request.user, from_user=user_id))   #, Q(to_user=request.user) | Q(from_user=user_id)

    #if recipient is selected, and there was no coversation with this recipient before, create new conversation
    if (user_id != None) and (Conversation.objects.filter(participants=sender).filter(participants=user_id).exists() != True):
        recipient = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.save()
        conversation.participants.add(recipient, sender)
    else:
        #get
        conversation = Conversation.objects.get(participants=sender)

    #If selected recipient was not contacted before, mark him as new_recipient
    if (user_id != None) and (Conversation.objects.filter(participants=user_id).exists() != True): # !! recent people  --changed from last_conversation
        new_recipient = User.objects.get(pk=user_id)
    else:
        new_recipient = None

    #instantiate form object if form is filled
    form = SendMessageForm(request.POST or None)

    context = {'recent_people': recent_people,
               'last_conversation': last_conversation,
               'form': form,
               'new_recipient': new_recipient
    }
    #if recepient is selected
    if user_id != None:

        #mark all 'unread' messages sent from this recepient as 'read'
        for message in last_conversation:
            if (message.status == 'unread') and (message.from_user != request.user):
                message.status = 'read'
                message.save()
        #selected recepient
        recipient = User.objects.get(pk=user_id)

        # if there is a message, and message is valid, send message to recepient selected
        if form.is_valid():
            #
            message = form.save(commit=False)
            message.from_user  = request.user
            message.to_user    =  recipient
            message.conversation = conversation
            message.save()
            return redirect('messages', user_id)

        #render the same page with empty form
        else:
            return render(request, 'messaging/messages.html', context)


    return render(request, 'messaging/messages.html', context)

'''
