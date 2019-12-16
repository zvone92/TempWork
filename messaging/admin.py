from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'message', 'timestamp', 'status')



admin.site.register(Message, MessageAdmin)
