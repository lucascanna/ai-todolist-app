from django.http import HttpResponse

from backend.models import Task, User
from backend.serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.
class Index(APIView):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the backend index")

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        task = self.get_object(pk)
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

