from django import forms
from .models import Worker

class WorkerCreateForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ['name', 'dob', 'skill', 'details', 'status']