from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView

from .models import TodoList
from django.views import View
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic.edit import ModelFormMixin


class LoginView(BaseLoginView):
    template_name = 'todo_list/login.html'
    redirect_authenticated_user = True
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('tasks')


class TasksViewList(ListView):
    model = TodoList
    context_object_name = 'tasks'
    paginate_by = 5
    ordering = ['created']

class TaskDetailView(DetailView):
    model = TodoList
    context_object_name = 'task_detail'


class CreateTaskView(CreateView):
    model = TodoList
    fields = ['user', 'title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

class UpdateTaskView(UpdateView):
    model = TodoList
    fields = ['user', 'title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
class DeleteTaskView(DeleteView):
    model = TodoList
    success_url = '/'

    
