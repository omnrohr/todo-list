from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import TodoList
from django.views import View
# Create your views here.
from django.views.generic.edit import ModelFormMixin
class TasksViewList(ListView):
    model = TodoList
    context_object_name = 'tasks'
    paginate_by = 5
    ordering = ['created']

class TaskDetailView(DetailView):
    model = TodoList
    context_object_name = 'task_detail'
