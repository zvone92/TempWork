from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileEditForm, UserEditForm
from django.contrib.auth.decorators import login_required
from temp.models import Profile


def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Profile.objects.create(user=new_user) # creating user profile
            messages.success(request, 'You are registered !')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html' ,{'form': form})

@login_required
def edit_profile(request):
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    user_form = UserEditForm(request.POST or None,  instance=request.user)
    if profile_form.is_valid() and user_form.is_valid():
        profile_form.save()
        user_form.save()
        messages.success(request, 'Successfully updated !')
        return redirect('home')

    else:
        return render(request, 'users/edit_profile.html', {'profile_form': profile_form, 'user_form': user_form })
