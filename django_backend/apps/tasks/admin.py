from django.contrib import admin
from .models import (
    Tag,
    Task,
    Comment,
    TaskTemplate
)

admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(TaskTemplate)