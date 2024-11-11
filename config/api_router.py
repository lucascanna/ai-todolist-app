from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ai_todo_list_app.tasks.views import TaskViewSet
from ai_todo_list_app.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("tasks", TaskViewSet)


app_name = "api"
urlpatterns = router.urls
