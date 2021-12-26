from django.urls.conf import path
from .views import DeleteTaskView, LoginView, TasksViewList, TaskDetailView, CreateTaskView, UpdateTaskView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', TasksViewList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('create/', CreateTaskView.as_view(), name='create-task'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='update-task'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete-task'),
]