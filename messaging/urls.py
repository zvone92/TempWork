from . import views
from django.urls import path

urlpatterns = [
    #path('messages/<int:recipient_id>', views.messages, name='messages'),
    #path('messages/', views.messages, name='messages'),

    path('conversation_list/', views.conversation_list, name='conversation_list'),
    path('message_box/<int:recipient_id>', views.message_box, name='message_box')
]
