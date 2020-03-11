from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Worker, Profile
from .forms import WorkerCreateForm, UpdateImageForm, EditWorkerInfoForm
from django.db.models import Q
from messaging.msg_util import new_messages


@login_required
def home(request):
    '''All workers ads are showing here'''
    workers = Worker.objects.all()
    query   = request.GET.get('q')
    if query:
        workers  = Worker.objects.filter(
        Q(skill__icontains=query)|
        Q(details__icontains=query)|
        Q(name__icontains=query))

    inbox = new_messages(request.user)

    context = {
                'workers': workers,
                'inbox': inbox
    }
    return render(request, 'temp/home.html', context)

def worker_profile(request):
    worker  = Worker.objects.get(user=request.user)
    '''Get object by id ,edit/change object data and save it to db'''
    form = UpdateImageForm(request.POST or None, request.FILES or None, instance=worker)

    if form.is_valid():
        form.save()
        return redirect('worker_profile')

    context = { 'worker': worker,
                'form':form,
    }

    return render(request, 'temp/worker_profile.html', context)


def worker_details(request, worker_id, slug):
    '''Show details about worker from id passed in request'''
    worker  = get_object_or_404(Worker, pk=worker_id)   # Get object by this id.
    context = {
        'worker': worker,
    }
    return render(request, 'temp/worker_details.html', context)


def create_worker(request):
    form = WorkerCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        worker = form.save(commit=False)   # commit=False tells Django not to send this to database yet, until i make some changes to it.
        worker.user  = request.user # Set the user object
        worker.save() # Now save it to database
        return redirect('home')

    else:
        return render(request, 'temp/create_worker.html', {'form':form})


def edit_worker_info(request):
    worker  = Worker.objects.get(user=request.user)
    form = EditWorkerInfoForm(request.POST or None, request.FILES or None, instance=worker)
    if form.is_valid():
        print('form is valid')
        form.save() # Now save it to database
        print('saved woker info')
        return redirect('worker_profile')

    else:
        return render(request, 'temp/edit_worker_info.html', {'form':form})
