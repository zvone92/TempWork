from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Worker, Profile
from .forms import WorkerCreateForm, ProfileImageForm, CoverImageForm, EditWorkerInfoForm
from django.db.models import Q
from messaging.msg_util import new_messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages

def home(request):
    '''
    Worker profiles are showing here so
    users can search for Workers
    '''
    # if user is registered
    if request.user.is_authenticated:
        workers = Worker.objects.exclude(user=request.user).filter(status='published').order_by('-pk')[0:9]
        # checking for new messages, returns integer
        inbox = new_messages(request.user)

    else:
        workers = Worker.objects.filter(status='published').order_by('-pk')[0:9]
        inbox = 0

    context = {
                'workers': workers,
                'inbox': inbox
    }
    return render(request, 'temp/home.html', context)


'''
def search(request):
    # if user is registered
    if request.user.is_authenticated:
        workers = Worker.objects.exclude(user=request.user).filter(status='published').order_by('-pk')[0:9]
        # checking for new messages, returns integer
        inbox = new_messages(request.user)

    else:
        workers = Worker.objects.filter(status='published').order_by('-pk')[0:9]
        inbox = 0

    query   = request.GET.get('q')

    if query:
        workers  = Worker.objects.filter(
        Q(skill__icontains=query)|
        Q(details__icontains=query)|
        Q(name__icontains=query),status='published')


    context = {
                'workers': workers,
                'inbox': inbox,
                'query': query
    }

    return render(request, 'temp/search.html', context)
'''

def search(request):
    query   = request.GET.get('q')
    inbox = 0
    # user is registered
    if request.user.is_authenticated:
        inbox = new_messages(request.user) # check for new messages
        if query:
            ''' if there is a search query, find by skill, details or name
                and show only published profiles. Exclude user.
            '''
            workers  = Worker.objects.exclude(user=request.user).filter(
            Q(skill__icontains=query)|
            Q(details__icontains=query)|
            Q(name__icontains=query),status='published')

        else:
            # show default profiles
            workers = Worker.objects.exclude(user=request.user).filter(status='published').order_by('-pk')[0:9]

    # unregistered user
    else:
        if query:
            ''' if there is a search query, find by skill, details or name
                and show only published profiles
            '''
            workers  = Worker.objects.filter(
            Q(skill__icontains=query)|
            Q(details__icontains=query)|
            Q(name__icontains=query),status='published')

        else:
            # show default profiles
            workers = Worker.objects.filter(status='published').order_by('-pk')[0:9]
    
    context = {
                'workers': workers,
                'inbox': inbox,
                'query': query
    }

    return render(request, 'temp/search.html', context)



@login_required
def worker_profile(request):
    '''
     worker profile page with edit options
     user can update/change profile image or cover image
    '''
    worker  = Worker.objects.get(user=request.user)
    profile_img_form = ProfileImageForm(request.POST or None, request.FILES or None, instance=worker)
    cover_img_form   = CoverImageForm(request.POST or None, request.FILES or None, instance=worker)

    if profile_img_form.is_valid() and cover_img_form.is_valid():
        profile_img_form.save()
        cover_img_form.save()
        messages.success(request, 'Image updated!')
        return redirect('worker_profile')

    context = { 'worker': worker,
                'profile_img_form': profile_img_form,
                'cover_img_form': cover_img_form,
    }

    return render(request, 'temp/worker_profile.html', context)


@login_required
def worker_details(request, worker_id, slug):
    '''
    Show details about worker from id passed in request
    '''
    worker  = get_object_or_404(Worker, pk=worker_id)
    context = {
        'worker': worker,
    }
    return render(request, 'temp/worker_details.html', context)


@login_required
def create_worker(request):
    '''
    creating Worker profile
    '''
    try:
        # Check if user already has a profile
        request.user.worker
    except ObjectDoesNotExist:
        pass
    else:
        return redirect('worker_profile')

    form = WorkerCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        worker = form.save(commit=False)
        worker.user  = request.user
        worker.save()
        messages.success(request, 'Profile created !')
        return redirect('home')

    else:
        return render(request, 'temp/create_worker.html', {'form':form})


@login_required
def edit_worker_info(request):
    '''
    editing basic information about worker
    '''
    worker  = Worker.objects.get(user=request.user)
    form = EditWorkerInfoForm(request.POST or None, request.FILES or None, instance=worker)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated !')
        return redirect('worker_profile')

    else:
        return render(request, 'temp/edit_worker_info.html', {'form':form})
