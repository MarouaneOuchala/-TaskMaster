from django.contrib import admin
from .models import Task, Category, TaskComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'category', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'category', 'user', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('user', 'category', 'parent_task')
    date_hierarchy = 'created_at'


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'task__title', 'user__username')
    raw_id_fields = ('task', 'user')
    date_hierarchy = 'created_at' 