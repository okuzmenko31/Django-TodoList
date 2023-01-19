import random
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import Registration, Authentication, TaskCreation, TaskUpdate, UserPasswordChange, UserResetPassword, \
    UserChangeEmail
from .tasks import *
from .models import Todo, Category


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('user_tasks')
    else:
        if request.method == 'POST':
            form = Registration(request.POST)
            if form.is_valid():
                users_emails = []
                for item in User.objects.all():
                    users_emails.append(item.email)
                if form.cleaned_data['email'] in users_emails:
                    messages.error(request, 'User with this email is already exists')
                    return redirect(request.path)
                else:
                    user = form.save()
                    login(request, user)
                    messages.success(request, 'You successfully created account')
                    send_registration_mail.delay(user.username, user.email)
                    return redirect('user_tasks')
        else:
            form = Registration()
        return render(request, 'Todo/registration_page.html', {'form': form})


def user_login(request):
    reset_form = UserResetPassword()
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
        return render(request, 'Todo/authentication_page.html', {'form': form, 'reset_form': reset_form})


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

            task_creation_mail.delay(request.user.username, request.user.email, task.title, task.description,
                                     task.category.name)

            messages.success(request, f'Task created successfully')
            return redirect('user_tasks')

    else:
        form = TaskCreation()
    return render(request, 'Todo/task_creation.html', {'form': form})


@login_required(login_url='/my_todolist/registration')
def user_tasks(request):
    tasks = Todo.objects.filter(user=request.user).select_related('category')

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


@login_required(login_url='/my_todolist/registration')
def task_update(request, task_id, cat_slug):
    task = Todo.objects.get(id=task_id, user=request.user)

    task_title = task.title
    task_desc = task.description
    task_cat = task.category
    task_date = task.date

    cat_slug = Category.objects.get(slug=cat_slug)

    if request.method == 'POST':
        form = TaskUpdate(request.POST)
        if form.is_valid():
            task.title = form.cleaned_data['title'] or task_title
            task.complete = form.cleaned_data['complete']
            task.description = form.cleaned_data['description'] or task_desc
            task.category = form.cleaned_data['category'] or task_cat
            task.date = form.cleaned_data['date'] or task_date
            task.save()

            task_updating_mail.delay(request.user.username, request.user.email, task.title)

            messages.success(request, 'Task was updated successfully')
            return redirect('user_tasks')
    else:
        form = TaskUpdate()
    return render(request, 'Todo/task_update.html', {'form': form, 'task': task})


@login_required(login_url='/my_todolist/registration')
def task_delete(request, task_id):
    task = Todo.objects.get(id=task_id, user=request.user)
    task.delete()

    return redirect('user_tasks')


@login_required(login_url='/my_todolist/registration')
def tasks_by_category(request, cat_id, cat_slug):
    category = Category.objects.get(id=cat_id, slug=cat_slug)
    tasks = Todo.objects.filter(user=request.user, category_id=cat_id).select_related('category')

    context = {
        'category': category,
        'tasks': tasks
    }
    return render(request, template_name='Todo/tasks_by_category.html', context=context)


@login_required(login_url='/my_todolist/authentication')
def user_profile(request):
    form = UserPasswordChange(user=request.user)
<<<<<<< HEAD
    context = {
        'form': form,
=======
    reset_form = UserResetPassword()
    change_email_form = UserChangeEmail()
    context = {
        'form': form,
        'reset_form': reset_form,
        'change_email_form': change_email_form
>>>>>>> change_mail
    }

    return render(request, template_name='Todo/user_page.html', context=context)


@login_required(login_url='/my_todolist/authentication')
def user_change_password(request):
    if request.method == 'POST':
        form = UserPasswordChange(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully changed your password!')
    return redirect('authentication')


def reset_password_page(request):
    reset_form = UserResetPassword()
    return render(request, 'Todo/reset_form_page.html', {'reset_form': reset_form})


def user_reset_password(request):
    if request.method == 'POST':
        reset_form = UserResetPassword(request.POST)
        if reset_form.is_valid():
            mail = reset_form.cleaned_data['email']

            user = User.objects.get(email=mail)

            if user:
                subject = 'Requested password reset'
                email_template_name = 'Todo/reset_password_mail.html'
                cont = {
                    'email': mail,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'TodoList',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                msg_html = render_to_string(email_template_name, cont)
                send_mail(subject, 'ссылка', 'kuzmenkowebdev@gmail.com', [mail], fail_silently=False,
                          html_message=msg_html)
                messages.success(request, 'Mail was sent successfully!')
    return redirect('authentication')


def user_change_email(request):
    code = random.randint(1000, 9999)
    request.session['change_code'] = str(code)

    subject = 'You send request for changing your email address at the TodoList site'
    message = f'Your code: {code}'
    send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [request.user.email], fail_silently=False)
    messages.success(request, 'Mail with the code was sent successfully!')

    return redirect('account')


def change_email_process(request):
    if request.method == 'POST':
        change_email_form = UserChangeEmail(request.POST)
        if change_email_form.is_valid():
            code = change_email_form.cleaned_data['code']
            if code == request.session['change_code']:
                del request.session['change_code']
                request.user.email = change_email_form.cleaned_data['new_email']
                request.user.save()
                messages.success(request, 'You successfully changed your email!')
            else:
                messages.error(request, 'The code is wrong, write it again')
    return redirect('account')
