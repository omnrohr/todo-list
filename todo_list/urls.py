from django.urls.conf import path
from .views import DeleteTaskView, TasksViewList, TaskDetailView, CreateTaskView, UpdateTaskView

urlpatterns = [
    path('', TasksViewList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('create/', CreateTaskView.as_view(), name='create-task'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='update-task'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete-task'),
]