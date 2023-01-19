from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Name of tasks category')
    slug = models.SlugField(unique=True, verbose_name='Category slug', blank=True)

    def __str__(self):
        return f'Category: {self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='User')
    title = models.CharField(max_length=450, verbose_name='Title of task')
    description = models.TextField(blank=True, verbose_name='Description of task')
    complete = models.BooleanField(default=False, verbose_name='The task completed or not?')
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now().strftime('%Y-%m-%d'), verbose_name='Date of task creation',
                            blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Category')

    def __str__(self):
        return f'User: {self.user.username}, task: {self.title}'

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'
        ordering = ['-created']
