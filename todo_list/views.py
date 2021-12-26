from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView

from django.contrib.auth.mixins import LoginRequiredMixin

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


class TasksViewList(LoginRequiredMixin, ListView):
    model = TodoList
    context_object_name = 'tasks'
    ordering = ['created']

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['completed'] = TodoList.objects.filter(user=self.request.user, completed=True)
        context['completed_count'] = context['completed'].count()
        context['in_porgress'] = TodoList.objects.filter(user=self.request.user, completed=False)
        context['in_porgress_count'] = context['in_porgress'].count()
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = TodoList
    context_object_name = 'task_detail'


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = TodoList
    fields = ['user', 'title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = TodoList
    fields = ['user', 'title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = TodoList
    success_url = '/'

    
