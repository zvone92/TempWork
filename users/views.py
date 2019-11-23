from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from temp.models import Profile

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            #username = form.cleaned_data.get('username')
            #password1 = form.cleaned_data.get('password1')
            print(form)
            Profile.objects.create(user=new_user)
            messages.success(request, 'Account created, you can now log in')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html' ,{'form': form})
