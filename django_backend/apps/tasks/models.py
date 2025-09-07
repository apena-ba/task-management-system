from django.db import models
from django.conf import settings


class Tag(models.Model):
    """
    Represents a tag that can be associated with tasks.
    Used for categorization, filtering, and searching.
    """

    # Core fields
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#FFFFFF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a task within the system.
    Supports assignment, tagging, and hierarchical parent-child relationships.
    """

    STATUS_CHOICES = [
        ("todo", "Task pending to be done"),
        ("in_progress", "Task in progress"),
        ("done", "Completed task")
    ]

    PRIORITY_CHOICES = [
        ("low", "Low priority"),
        ("medium", "Medium priority"),
        ("high", "High priority")
    ]

    # Core fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateTimeField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Relationships
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks_created",
    )
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks_assigned",
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        blank=True,
    )
    parent_task = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subtasks",
    )

    # Metadata
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        db_table = "tasks"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["due_date"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"


class Comment(models.Model):
    """
    Represents a comment made on a task by a user.
    """
    
    # Core fields
    content = models.TextField()

    # Relationships
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.created_by} on {self.task}"


class TaskTemplate(Task):
    """
    Template for tasks.
    Inherits all fields from Task but is stored separately in its own table.
    Used to create new tasks based on pre-defined templates.
    """
    class Meta:
        db_table = "task_templates"
        ordering = ["title"]

    def __str__(self):
        return f"Template: {self.title}"
