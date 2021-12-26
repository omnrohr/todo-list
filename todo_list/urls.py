from django.urls.conf import path
from .views import TasksViewList, TaskDetailView

urlpatterns = [
    path('', TasksViewList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task'),

]