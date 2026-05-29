from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # <-- Protects views
from .models import Task
from django.contrib.auth.forms import UserCreationForm

@login_required(login_url='/login/') # Redirects to login page if not logged in
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            # SQL INSERT: Saves the task AND links it to the logged-in user
            Task.objects.create(title=title, user=request.user) 
        return redirect('task_list')

    # SQL SELECT: Only grabs tasks where user matches the logged-in user!
    tasks = Task.objects.filter(user=request.user) 
    return render(request, 'todo/tasks.html', {'tasks': tasks})

@login_required(login_url='/login/')
def complete_task(request, task_id):
    if request.method == "POST":
        # Security: ensures a user can't modify someone else's task ID
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.is_completed = True
        task.save()
    return redirect('task_list')

@login_required(login_url='/login/')
def delete_task(request, task_id):
    if request.method == "POST":
        # Security: ensures a user can't delete someone else's task ID
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
    return redirect('task_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # This automatically handles the SQL INSERT into the user table!
            return redirect('login') # Send them straight to the login page
    else:
        form = UserCreationForm()
        
    return render(request, 'todo/register.html', {'form': form})