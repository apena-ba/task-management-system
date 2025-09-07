from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import (
    TaskSerializer,
    TaskAssignSerializer,
    CommentSerializer,
)
from .models import (
    Task,
    Comment,
)
from .filters import TaskFilter


# Route   -> /api/tasks/
# Methods -> GET POST
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Route   -> /api/tasks/{id}/
# Methods -> GET PUT PATCH DELETE
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


# Route   -> /api/tasks/{id}/assign/
# Methods -> POST
class TaskAssignView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskAssignSerializer

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Task assignments updated successfully."}, status=status.HTTP_200_OK)


# Route   -> /api/tasks/{id}/comments/
# Methods -> GET POST
class TaskCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs["pk"]
        return Comment.objects.filter(task_id=task_id).order_by("-created_at")

    def perform_create(self, serializer):
        task_id = self.kwargs["pk"]
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(task=task, created_by=self.request.user)
