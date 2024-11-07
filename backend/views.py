from django.http import HttpResponse

from backend.models import Task, User
from backend.serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class Index(APIView):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the backend index")

class TaskList(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        task = TaskSerializer(tasks, many=True)
        return Response(task.data)
    def post(self, request):
        task_serializer = TaskSerializer(data=request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetail(APIView):
    def get_object(self, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, task_id):
        task = self.get_object(task_id)
        task_serializer = TaskSerializer(task)
        return Response(task_serializer.data)
    def delete(self, request, task_id):
        task = self.get_object(task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self, request, task_id):
        task = self.get_object(task_id)
        task_serializer = TaskSerializer(task, data=request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, task_id):
        task = self.get_object(task_id)
        task_serializer = TaskSerializer(task, data=request.data, partial=True)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        user = UserSerializer(users, many=True)
        return Response(user.data)
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

