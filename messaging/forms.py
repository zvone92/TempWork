from django import forms
from .models import Message

class SendMessageForm(forms.ModelForm):

    class Meta:
        model = Message

        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Write message', 'rows': 1, 'cols': 40}),
        }

        fields = ['message']
        labels = {'message': ''}
