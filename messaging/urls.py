from . import views
from django.urls import path

urlpatterns = [
    path('messages/<int:user_id>', views.messages, name='messages'),
    path('messages/', views.messages, name='messages')
]
