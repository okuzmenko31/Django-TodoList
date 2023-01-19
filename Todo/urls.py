from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', user_tasks, name='user_tasks'),
    path('registration/', user_registration, name='registration'),
    path('authentication/', user_login, name='authentication'),
    path('task_creation/', user_task_creation, name='task_creation'),
    path('logout/', user_logout, name='logout'),
    path('category/<slug:cat_slug>/task/<int:task_id>/', task_detail, name='detail'),
    path('category/<slug:cat_slug>/task/<int:task_id>/update/', task_update, name='update'),
    path('task_delete/task/<int:task_id>/', task_delete, name='delete'),
    path('tasks/<slug:cat_slug>/<int:cat_id>/', tasks_by_category, name='by_category'),
    path('account_settings/', user_profile, name='account'),
    path('user_change_password/', user_change_password, name='change_password'),
    path('user_reset_password/', user_reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='Todo/confirmation.html'),
         name='confirmation'),
    path('reset/done/', views.PasswordResetDoneView.as_view(template_name='Todo/reset_done.html'),
         name='password_reset_complete'),
    path('mail_change/', user_change_email, name='change_email'),
    path('mail_change_process/', change_email_process, name='change_email_process')
]
