from django import forms
from .models import Worker
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class WorkerCreateForm(forms.ModelForm):


    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'placeholder': (u'Cellphone'), 'class':"form-control"}),
                       label= (u''), required=False, initial='+52')

    BIRTH_YEAR_CHOICES = [str(i) for i in range(1940,2000)] #['1990', '1991', '1992']
    dob = forms.DateField(
                widget=forms.SelectDateWidget(
                        empty_label=("Choose Year", "Choose Month", "Choose Day"),
                        years=BIRTH_YEAR_CHOICES
                ), label='')

    class Meta:
        model = Worker
        fields = ['name', 'lastname', 'dob', 'image', 'skill', 'details', 'status', 'hourly_rate', 'phone']
        labels = {'name': '', 'lastname': '', 'skill': '', 'details': '', 'status': '', 'hourly_rate': ''}



    #attrs={'type': 'date'},
    # ,input_formats=('%m/%d/%Y', ))
