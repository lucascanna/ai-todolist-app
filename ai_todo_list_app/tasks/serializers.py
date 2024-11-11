from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(source="owner.email", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["owner"]


class CreateTaskWithAISerializer(serializers.Serializer):
    message = serializers.CharField()
