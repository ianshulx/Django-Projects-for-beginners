from django.contrib import admin

from .models import Task

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "is_completed",
        "priority",
        "due_date",
        "created_at",
    )
    list_filter = ("is_completed", "priority", "due_date")
    search_fields = ("title", "description")
