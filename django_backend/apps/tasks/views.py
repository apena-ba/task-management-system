from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from apps.authentication.decorators import jwt_login_required
from django.conf import settings
from django.http import FileResponse, Http404
from django.views import View
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

import os


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


# Route   -> /tasks/
@method_decorator(jwt_login_required, name='dispatch')
class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all().select_related("created_by").prefetch_related("assigned_to", "tags")
        return render(request, "task_list.html", {"tasks": tasks})


# Route   -> /tasks/{id}/
@method_decorator(jwt_login_required, name='dispatch')
class TaskDetailTemplateView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task.objects.select_related("created_by"), pk=pk)
        return render(request, "task_detail.html", {"task": task})


# Route   -> /tasks/create/
@method_decorator(jwt_login_required, name='dispatch')
class TaskCreateTemplateView(View):
    def get(self, request):
        return render(request, "task_create.html")


# Route -> /reports/
@method_decorator(jwt_login_required, name="dispatch")
class ReportsTemplateView(View):
    def get(self, request):
        shared_dir = '/shared'
        try:
            files = [f for f in os.listdir(shared_dir) if os.path.isfile(os.path.join(shared_dir, f))]
        except FileNotFoundError:
            files = []
        return render(request, "reports.html", {"files": files})


# Route -> /reports/download/<filename>/
@method_decorator(jwt_login_required, name="dispatch")
class ReportDownloadView(View):
    def get(self, request, filename):
        shared_dir = '/shared'
        file_path = os.path.join(shared_dir, filename)

        # Prevent path traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(shared_dir)):
            raise Http404("File not found.")

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise Http404("File not found.")

        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)