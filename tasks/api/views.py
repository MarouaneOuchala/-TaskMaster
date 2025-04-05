from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status = request.query_params.get('status', 'todo')
        tasks = self.get_queryset().filter(status=status)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        priority = request.query_params.get('priority', 'medium')
        tasks = self.get_queryset().filter(priority=priority)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 