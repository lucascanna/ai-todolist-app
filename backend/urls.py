from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('tasks', views.task_list, name='task_list'),
    path('users', views.user_list, name='user_list'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
]
