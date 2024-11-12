import pytest
from django.db import connection

from ai_todo_list_app.users.models import User
from ai_todo_list_app.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(autouse=True)
def _reset_sequences(django_db_reset_sequences):
    """Reset database sequences before each test."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT setval(pg_get_serial_sequence('tasks_task', 'id'), 1, false);",
        )


@pytest.fixture
def user(db) -> User:
    return UserFactory()
