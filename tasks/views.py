from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from .forms import TaskForm
from .models import Task


def toggle_task_status(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        previous_status = task.status
        is_checked = request.POST.get('completed') == 'true'

        if is_checked:
            task.status = 'Completed'
        else:
            task.status = 'Pending' if previous_status == 'Completed' else previous_status

        task.save()
        return JsonResponse({'success': True, 'new_status': task.status})

    return JsonResponse({'success': False}, status=400)



def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully!")
            return redirect('task_list')  # You'll define this URL later
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})

def toggle_task_status(request, pk):
    if request.method == 'POST':
        try:
            task = get_object_or_404(Task, pk=pk)
            is_checked = request.POST.get('completed')

            if is_checked not in ['true', 'false']:
                raise ValueError("Invalid value for 'completed' checkbox.")

            is_checked = is_checked == 'true'
            previous_status = task.status

            task.status = 'Completed' if is_checked else 'Pending' if previous_status == 'Completed' else previous_status
            task.save()

            return JsonResponse({'success': True, 'new_status': task.status})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


def delete_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        messages.success(request, "Task deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting task: {str(e)}")
    return redirect('task_list')


def task_list(request):
    tasks = Task.objects.all()
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    due_date = request.GET.get('due_date')

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    if due_date:
        try:
            parsed_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            tasks = tasks.filter(due_date__lte=parsed_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")

    context = {
        'tasks': tasks,
        'status_filter': status,
        'priority_filter': priority,
        'due_date_filter': due_date,
    }
    return render(request, 'tasks/task_list.html', context)