from django.shortcuts import render
from django.http import HttpResponse

from backend.models import Task, User
from backend.serializers import TaskSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the backend index")

@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        task = TaskSerializer(tasks, many=True)
        return JsonResponse(task.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        task_serializer = TaskSerializer(data=data)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse(task_serializer.data, status=201)
        return JsonResponse(task_serializer.errors, status=400)
    
@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        task_serializer = TaskSerializer(task)
        return JsonResponse(task_serializer.data)
    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=204)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        task_serializer = TaskSerializer(task, data=data)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse(task_serializer.data, status=201)
        return JsonResponse(task_serializer.errors, status=400)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        task_serializer = TaskSerializer(task, data=data, partial=True)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse(task_serializer.data, status=201)
        return JsonResponse(task_serializer.errors, status=400)
    
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        user = UserSerializer(users, many=True)
        return JsonResponse(user.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        user = UserSerializer(data=data)
        if user.is_valid():
            user.save()
            return JsonResponse(user.data, status=201)
        return JsonResponse(user.errors, status=400)

