from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'tasks'

def redirect_task_detail(request, pk):
    return redirect('tasks:task-detail', pk=pk)

urlpatterns = [
    # Task URLs
    path('', views.TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/update-status/', views.update_task_status, name='task-update-status'),
    path('<int:pk>/', redirect_task_detail, name='task-detail-redirect'),  # Redirect old URL format
    
    # Category URLs
    path('categories/', views.category_list, name='category-list'),
    path('category/new/', views.category_create, name='category-create'),
    path('category/<int:pk>/update/', views.category_update, name='category-update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category-delete'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('day/<int:year>/<int:month>/<int:day>/', views.day_tasks, name='day-tasks'),
] 