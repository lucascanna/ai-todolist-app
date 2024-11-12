import json
import os

from premai import Prem
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import CreateTaskWithAISerializer
from .serializers import TaskSerializer

prem_client = Prem(api_key=os.environ["PREM_API_KEY"])
prem_project_id = os.environ["PREM_PROJECT_ID"]


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    system_prompt = """
    Create a task object in JSON format.
    The task object should have title and description fields.
    The title and description should be extracted from the following sentence.
    Your response contain only JSON and nothing else.
    """

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    @action(detail=False, methods=["post"])
    def ai(self, request):
        serializer = CreateTaskWithAISerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data["message"]
            response = prem_client.chat.completions.create(
                project_id=prem_project_id,
                messages=[{"role": "user", "content": message}],
                system_prompt=self.system_prompt,
            )
            task_data = json.loads(response.choices[0].message.content)
            serializer = TaskSerializer(data=task_data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
