from django import forms
from .models import Worker
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class WorkerCreateForm(forms.ModelForm):

    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'placeholder': (u'Cellphone'), 'class':"form-control"}),
                       label= (u''), required=False, initial='+52')

    BIRTH_YEAR_CHOICES = [str(i) for i in range(2005, 1950, -1 )]
    dob = forms.DateField(
                widget=forms.SelectDateWidget(
                        empty_label=("Choose Year", "Choose Month", "Choose Day"),
                        years=BIRTH_YEAR_CHOICES
                ), label='')

    class Meta:
        model = Worker
        fields = ['name', 'lastname', 'dob', 'skill', 'details', 'status', 'image', 'hourly_rate', 'phone']
        labels = {'name': '', 'lastname': '', 'skill': '', 'details': '', 'status': '', 'hourly_rate': ''}



class EditWorkerInfoForm(forms.ModelForm):

        phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'placeholder': (u'Cellphone'), 'class':"form-control"}),
                           label= (u''), required=False, initial='+52')

        BIRTH_YEAR_CHOICES = [str(i) for i in range(2005, 1950, -1 )] #['1990', '1991', '1992']
        dob = forms.DateField(
                    widget=forms.SelectDateWidget(
                            empty_label=("Choose Year", "Choose Month", "Choose Day"),
                            years=BIRTH_YEAR_CHOICES
                    ), label='')

        class Meta:
            model = Worker
            exclude = ('user', 'image', 'cover', 'slug', 'created', 'medals', )
            labels = {'name': '', 'lastname': '', 'skill': '', 'details': '', 'status': '', 'hourly_rate': ''}



class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ['image']
        labels = {'image': ''}
        '''
        widgets = {'image':forms.FileInput(
        attrs={'style':'display: none;','class':'form-control', 'required': False}
        )}
        '''


class CoverImageForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ['cover']
