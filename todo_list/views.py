from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView as BaseLoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import TodoList
from django.views import View
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic.edit import ModelFormMixin
from django.db import transaction
from .forms import PositionForm


class LoginView(BaseLoginView):
    template_name = 'todo_list/login.html'
    redirect_authenticated_user = True
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('tasks')


class UserCreationView(FormView):
    template_name = 'todo_list/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('create-task')
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        else:
            redirect('register')
        return super(UserCreationView, self).form_valid(form)



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
        search_field = self.request.GET.get('search-area') or ''
        if search_field:
            context['tasks'] = context['tasks'].filter(user=self.request.user).filter(title__icontains=search_field)
            context['completed'] = TodoList.objects.filter(user=self.request.user, completed=True).filter(title__icontains=search_field)
            context['completed_count'] = context['completed'].count()
            context['in_porgress'] = TodoList.objects.filter(user=self.request.user, completed=False).filter(title__icontains=search_field)
            context['in_porgress_count'] = context['in_porgress'].count()
            context['search_input'] = search_field
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = TodoList
    context_object_name = 'task_detail'


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = TodoList
    fields = [ 'title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = TodoList
    fields = [ 'title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = TodoList
    success_url = '/'

    
class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_todolist_order(positionList)

        return redirect(reverse_lazy('tasks'))