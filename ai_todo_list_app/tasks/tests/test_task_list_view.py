from django.test import TestCase
from freezegun import freeze_time
from rest_framework import status

from ai_todo_list_app.tasks.models import Task
from ai_todo_list_app.users.models import User


# Create your tests here.
class TaskListViewTests(TestCase):
    @freeze_time("2024-11-09")
    def setUp(self):
        authenticated_user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",  # noqa: S106
        )
        unauthenticated_user = User.objects.create_user(
            email="unauthenticateduser@example.com",
            password="unauthenticatedUser",  # noqa: S106
        )
        self.client.force_login(authenticated_user)
        Task.objects.create(
            title="Test Task 1",
            description="Test Task 1 Description",
            owner=authenticated_user,
        )
        Task.objects.create(
            title="Test Task 2",
            description="Test Task 2 Description",
            owner=authenticated_user,
        )
        Task.objects.create(
            title="Test Task 3",
            description="Test Task 3 Description",
            owner=unauthenticated_user,
        )

    @freeze_time("2024-11-09")
    def test_authenticated_user_only_views_his_tasks(self):
        response = self.client.get("/api/tasks/")
        expected_response = [
            {
                "id": 1,
                "title": "Test Task 1",
                "description": "Test Task 1 Description",
                "owner": "testuser@example.com",
                "status": "todo",
                "created_at": "2024-11-09T00:00:00Z",
                "updated_at": "2024-11-09T00:00:00Z",
            },
            {
                "id": 2,
                "title": "Test Task 2",
                "description": "Test Task 2 Description",
                "owner": "testuser@example.com",
                "status": "todo",
                "created_at": "2024-11-09T00:00:00Z",
                "updated_at": "2024-11-09T00:00:00Z",
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
