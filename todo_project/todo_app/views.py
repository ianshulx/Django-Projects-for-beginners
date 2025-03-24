from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    '''
    Bring the list of all the tasks.
    '''
    tasks = Task.objects.all().order_by('completed')
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})


def add_task(request):
    '''
    Add a new Task.
    '''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/add_task.html', {'form': form})


def update_task(request, pk):
    '''
    Update an existing task.
    '''
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo_app/update_task.html', {'form': form})


def delete_task(request, pk):
    '''
    Delete an existing task.
    '''
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')


def mark_completed(request, pk):
    '''
    Toggle between complete and uncomplete a task.
    '''
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
