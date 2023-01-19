from TodoList.celery import app
from django.core.mail import send_mail


@app.task
def send_registration_mail(user, user_email):
    subject = f'{user} - You successfully created account at the Todo List Site!'
    message = f'Now you can start creating your todo list. Dont forget to follow me on GitHub:\n' \
              f'https://github.com/okuzmenko31'
    send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [user_email], fail_silently=False)


@app.task
def task_creation_mail(user, user_email, task_title, task_description, task_category):
    subject = f'TODO LIST - {user}, You successfully created new task!'
    message = f'Your task:\n\n' \
              f'Task title: {task_title}\n' \
              f'Task description: {task_description}\n' \
              f'{task_category}\n\n\n'
    send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [user_email], fail_silently=False)


@app.task
def task_updating_mail(user, user_email, task_title):
    send_mail(f'{user} - Your task was updated successfully!',
              f'Your task: "{task_title}" was updated!',
              'kuzmenkowebdev@gmail.com', [user_email])
