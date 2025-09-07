import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Filters for Task list endpoint
    """

    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains",
        help_text="Filter tasks by title (case-insensitive search)"
    )
    status = django_filters.ChoiceFilter(
        field_name="status", choices=Task.STATUS_CHOICES,
        help_text="Filter tasks by status:"
    )
    priority = django_filters.ChoiceFilter(
        field_name="priority", choices=Task.PRIORITY_CHOICES,
        help_text="Filter tasks by priority:"
    )
    created_by = django_filters.NumberFilter(
        field_name="created_by__id",
        help_text="Filter tasks by the creator's user ID"
    )
    assigned_to = django_filters.NumberFilter(
        field_name="assigned_to__id",
        help_text="Filter tasks by assigned user ID"
    )
    due_date_before = django_filters.DateTimeFilter(
        field_name="due_date", lookup_expr="lte",
        help_text="Filter tasks due before this date"
    )
    due_date_after = django_filters.DateTimeFilter(
        field_name="due_date", lookup_expr="gte",
        help_text="Filter tasks due after this date"
    )

    class Meta:
        model = Task
        fields = ["title", "status", "priority", "created_by", "assigned_to"]
