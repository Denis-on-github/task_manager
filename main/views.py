from typing import cast

import django_filters

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main.models import Tag, Task, User
from main.permissions import IsStaffOrReadOnly
from main.serializers import TagSerializer, TaskSerializer, UserSerializer
from services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__id", to_field_name="id", queryset=Tag.objects.all()
    )
    executor = django_filters.ModelChoiceFilter(
        field_name="executor__id", to_field_name="id", queryset=User.objects.all()
    )
    author = django_filters.ModelChoiceFilter(
        field_name="author__id", to_field_name="id", queryset=User.objects.all()
    )

    class Meta:
        model = Task
        fields = ("status", "tags", "executor", "author")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.all().select_related("author", "executor").prefetch_related("tags")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
