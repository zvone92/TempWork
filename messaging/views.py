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
    # ELSE
        # GET RECIPIENT(USER) BY RECIPIENT ID
        # IF TEHERE IS NO THIS RECIPIENT IN CONVERSATIONS
        # CREATE CONVERSATION AND ADD RECIPIENT + CURRENT USER
        
    #ALL CONVERSATIONS THAT USER IS PARTICIPATING IN
    recent_conversations = Conversation.objects.filter(participants=user).order_by('-pk')

    # LAST MESSAGE FROM EACH CONVERSATION
    last_message = [(i.mesagges.last(), i.mesagges.last().correspondent(user)) for i in recent_conversations]

    # IF THERE IS NO RECIPIENT SELECTED, GET THE LAST CONVERSATION
    if recipient_id == None:
        last_conversation = recent_conversations.filter(participants=last_recipient).first()
        # IF PREVIOUS CONVERSATION EXISTS
        if last_conversation != None:
            #ALL MESSAGES FROM SELECTED CONVERSATION
            all_messages = last_conversation.mesagges.all()                     # READ ALL MESSAGES
        # THERE ARE NO PREVIOUS CONVERSATION
        else:
            all_messages= None

    # IF RECIPIENT SELECTED, GET CONVERSATION WITH THIS RECIPIENT
    else:
        last_conversation =  recent_conversations.filter(participants=recipient_id).first() #change from first()
        if last_conversation != None:
            #ALL MESSAGES FROM SELECTED CONVERSATION
            all_messages= last_conversation.mesagges.all()                      # READ ALL MESSAGES
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
        if form.is_valid():                                                      # IF THERE IS MESSAGE
            message = form.save(commit=False)
            message.from_user  =  user
            message.to_user    =  recipient
            message.save()                                                      # SAVE IT
            # CREATE CONVERSATION WITH THIS PERSON, IF IT DOESN'T EXISTS
            if recent_conversations.filter(participants=recipient).exists() != True: # bug:   # --- THIS ON BEGGINING OF VIEW
                #recipient = get_object_or_404(User, pk=recipient_id)
                conversation = Conversation.objects.create()
                conversation.save()
                conversation.participants.add(user, recipient) # lst point
            # ADD MESSAGE TO BELONGING CONVERSATION
            last_conversation = recent_conversations.filter(participants=recipient).first()    # AND ADD MESSAGE TO CONVERSATION
            if  last_conversation != None:
                last_conversation.mesagges.add(message)
            return redirect('messages', recipient.id)                                          # RETURN PAGE WITH SELECTED ID
        #render the same page with empty form
        else:
            print("here first")
            return render(request, 'messaging/messages.html', context)
    print("here second")
    return render(request, 'messaging/messages.html', context)
