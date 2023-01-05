from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category, Todo
from .forms import Registration, Authentication, TaskCreation, TaskUpdate


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('user_tasks')
    else:
        if request.method == 'POST':
            form = Registration(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                subject = f'{user.username} - You successfully created account at the Todo List Site!'
                message = f'Now you can start creating your todo list. Dont forget to follow me on GitHub:\n' \
                          f'https://github.com/okuzmenko31'
                send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [request.user.email])
                messages.success(request, 'You successfully created account')
                return redirect('user_tasks')
        else:
            form = Registration()
        return render(request, 'Todo/registration_page.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_tasks')
    else:
        if request.method == 'POST':
            form = Authentication(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'You successfully authenticated!')
                return redirect('user_tasks')
        else:
            form = Authentication()
        return render(request, 'Todo/authentication_page.html', {'form': form})


def user_task_creation(request):
    if request.method == 'POST':
        form = TaskCreation(request.POST)
        if form.is_valid():
            task = Todo()
            task.user = request.user
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.category = form.cleaned_data['category']
            task.save()

            subject = f'TODO LIST - {request.user.username} You successfully created new task!'
            message = f'Your task:\n\n' \
                      f'Task title: {task.title}\n' \
                      f'Task description: {task.description}\n' \
                      f'{task.category}\n\n\n'
            send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [request.user.email])

            messages.success(request, f'Task created successfully')
            return redirect('user_tasks')

    else:
        form = TaskCreation()
    return render(request, 'Todo/task_creation.html', {'form': form})


@login_required(login_url='/my_todolist/registration')
def user_tasks(request):
    tasks = Todo.objects.filter(user=request.user)

    return render(request, 'Todo/user_tasks.html', {'tasks': tasks})


@login_required(login_url='/my_todolist/registration')
def user_logout(request):
    logout(request)
    return redirect('authentication')


@login_required(login_url='/my_todolist/registration')
def task_detail(request, task_id, cat_slug):
    task = get_object_or_404(Todo, user=request.user, id=task_id)

    cat_slug = Category.objects.get(slug=cat_slug)

    return render(request, 'Todo/task_detail.html', {'task': task})


def task_update(request, task_id, cat_slug):
    task = Todo.objects.get(id=task_id, user=request.user)

    task_title = task.title
    task_desc = task.description
    task_cat = task.category
    # task_date = task.date

    cat_slug = Category.objects.get(slug=cat_slug)

    if request.method == 'POST':
        form = TaskUpdate(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title'] or task_title
            complete = form.cleaned_data['complete']
            description = form.cleaned_data['description'] or task_desc
            category = form.cleaned_data['category'] or task_cat
            # date = form.cleaned_data['date'] or task_date

            Todo.objects.update(id=task_id, user=request.user, title=title, complete=complete, description=description,
                                category=category)
            send_mail(f'{request.user.username} - Your task was updated successfully!',
                      f'Your task {title} was updated!',
                      'kuzmenkowebdev@gmail.com', [request.user.email])
            messages.success(request, 'Task was updated successfully')
            return redirect('user_tasks')
    else:
        form = TaskUpdate()
    return render(request, 'Todo/task_update.html', {'form': form, 'task': task})


def task_delete(request, task_id):
    task = Todo.objects.get(id=task_id, user=request.user)
    task.delete()

    return redirect('user_tasks')


def tasks_by_category(request, cat_id, cat_slug):
    category = Category.objects.get(id=cat_id, slug=cat_slug)
    tasks = Todo.objects.filter(user=request.user, category_id=cat_id)

    context = {
        'category': category,
        'tasks': tasks
    }
    return render(request, template_name='Todo/tasks_by_category.html', context=context)
