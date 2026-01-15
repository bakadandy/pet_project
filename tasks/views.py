from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet # gives you list, create, retrieve, update, delete
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.permissions import IsOwner


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self): # scopes data to the current user (security)
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer): # injects user safely (no client control)
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        cached_key = f"tasks:user:{user_id}"

        cached = cache.get(cached_key)
        if cached is not None:
            return Response(cached)

        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        data = serializer.data

        cache.set(cached_key, data, 60)
        return Response(data)
