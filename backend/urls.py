from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path('tasks', views.TaskList.as_view(), name='task_list'),
    path('users', views.UserList.as_view(), name='user_list'),
    path('tasks/<int:task_id>', views.TaskDetail.as_view(), name='task_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)