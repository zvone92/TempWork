from django.contrib import admin
from .models import Message, Conversation

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message','from_user', 'to_user', 'timestamp', 'status')



admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation)
