import os
from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from apps.tasks.models import Task


SHARED_PATH = "/shared"


@shared_task
def generate_daily_summary():
    """Generate daily task summary for all users"""

    today = datetime.now().date()
    tasks_due_today = (
        Task.objects.filter(due_date__date__lte=today, is_archived=False)
        .select_related("created_by", "parent_task")
        .prefetch_related("assigned_to", "tags")
    )

    filename = os.path.join(SHARED_PATH, f"daily_summary_{today}.txt")

    # Define template for each task
    task_template = (
        "- {title}\n"
        "  Status: {status} | Priority: {priority}\n"
        "  Created by: {created_by}\n"
        "  Assigned to: {assigned_to}\n"
        "  Tags: {tags}\n"
        "  Due: {due_date}\n\n"
    )

    with open(filename, "w") as f:
        f.write(f"📌 Daily Summary for {today}\n")
        f.write("=" * 50 + "\n\n")

        if not tasks_due_today.exists():
            f.write("No tasks due today.\n")
        else:
            for task in tasks_due_today:
                assigned_users = ", ".join([str(u) for u in task.assigned_to.all()]) or "Unassigned"
                tags = ", ".join([tag.name for tag in task.tags.all()]) or "No tags"

                f.write(
                    task_template.format(
                        title=task.title,
                        status=task.status,
                        priority=task.priority,
                        created_by=task.created_by,
                        estimated_hours=task.estimated_hours,
                        assigned_to=assigned_users,
                        tags=tags,
                        due_date=task.due_date.strftime("%Y-%m-%d %H:%M"),
                    )
                )

    return filename


@shared_task
def cleanup_archived_tasks():
    """Delete archived tasks older than 30 days"""

    cutoff = datetime.now() - timedelta(days=30)

    old_tasks = (
        Task.objects.filter(is_archived=True, due_date__lt=cutoff)
        .select_related("created_by", "parent_task")
        .prefetch_related("assigned_to", "tags")
    )

    count = old_tasks.count()

    # Log which tasks are being removed
    for task in old_tasks:
        assigned_users = ", ".join(str(u) for u in task.assigned_to.all()) or "Unassigned"
        print(f"Deleting task: {task.title} | Created by: {task.created_by} | Assigned to: {assigned_users}")

    old_tasks.delete()

    return f"Deleted {count} archived tasks older than {cutoff.date()}"