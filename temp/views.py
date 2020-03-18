from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Worker, Profile
from .forms import WorkerCreateForm, UpdateImageForm, EditWorkerInfoForm
from django.db.models import Q
from messaging.msg_util import new_messages


@login_required
def home(request):
    '''
    all worker profiles are showing here
    users can search for Workers
    '''
    workers = Worker.objects.all().exclude(user=request.user)
    query   = request.GET.get('q')
    # if there is a search query, find by skill, details or name
    if query:
        workers  = Worker.objects.filter(
        Q(skill__icontains=query)|
        Q(details__icontains=query)|
        Q(name__icontains=query))
    # checking for new messages, returns integer
    inbox = new_messages(request.user)

    context = {
                'workers': workers,
                'inbox': inbox
    }
    return render(request, 'temp/home.html', context)


@login_required
def worker_profile(request):
    '''
     worker profile page
     user can change image or info
    '''
    worker  = Worker.objects.get(user=request.user)
    form = UpdateImageForm(request.POST or None, request.FILES or None, instance=worker)

    if form.is_valid():
        form.save()
        return redirect('worker_profile')

    context = { 'worker': worker,
                'form':form,
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
    form = WorkerCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        worker = form.save(commit=False)
        worker.user  = request.user
        worker.save()
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
        print('form is valid')
        form.save()
        print('saved woker info')
        return redirect('worker_profile')

    else:
        return render(request, 'temp/edit_worker_info.html', {'form':form})
