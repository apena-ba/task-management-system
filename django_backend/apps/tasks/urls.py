from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    TaskAssignView,
    TaskCommentListCreateView,
)

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/assign/", TaskAssignView.as_view(), name="task-assign"),
    path("tasks/<int:pk>/comments/", TaskCommentListCreateView.as_view(), name="task-comments"),
]
