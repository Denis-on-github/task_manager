from rest_framework import viewsets

from main.models import User, Tag, Task
from main.serializers import UserSerializer, TagSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.all().select_related("author", "executor").prefetch_related("tags")
    )
    serializer_class = TaskSerializer
