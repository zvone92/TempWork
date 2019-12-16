from django import forms
from .models import Message

class SendMessageForm(forms.ModelForm):

    class Meta:
        model = Message

        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'Write message'}),
        }

        fields = ['message']
        labels = {'message': ''}
