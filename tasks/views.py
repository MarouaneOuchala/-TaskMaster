from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import Task, Category, TaskComment
from .forms import TaskForm, CategoryForm, TaskCommentForm, TaskShareForm
from datetime import timedelta, date
from django.core.serializers import serialize
import json
from django.core.paginator import Paginator


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_calendar.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()
        
        # Convert tasks to JSON for JavaScript
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'category': task.category.id if task.category else None,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            })
        
        context['tasks_json'] = json.dumps(tasks_data)
        context['categories'] = Category.objects.filter(user=self.request.user)
        return context


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('tasks:category-list')
    else:
        form = CategoryForm()
    return render(request, 'tasks/category_form.html', {'form': form})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('tasks:category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'tasks/category_form.html', {'form': form})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('tasks:category-list')
    return render(request, 'tasks/category_confirm_delete.html', {'category': category})


@login_required
def analytics_view(request):
    # Get total tasks and status distribution
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, status='completed').count()
    in_progress_tasks = Task.objects.filter(user=request.user, status='in_progress').count()
    todo_tasks = Task.objects.filter(user=request.user, status='todo').count()

    # Get category distribution
    categories = Category.objects.filter(user=request.user)
    category_distribution = []
    
    for category in categories:
        task_count = Task.objects.filter(user=request.user, category=category).count()
        if task_count > 0:  # Only include categories that have tasks
            category_distribution.append({
                'name': category.name,
                'task_count': task_count
            })
    
    # If no categories with tasks, add a default one to avoid JavaScript errors
    if not category_distribution:
        category_distribution.append({
            'name': 'No Tasks in Categories',
            'task_count': 0
        })

    # Get completion trends
    today = timezone.now()
    week_ago = today - timezone.timedelta(days=7)
    month_ago = today - timezone.timedelta(days=30)

    # Fix: Use a simpler approach for counting completed tasks
    weekly_completion = Task.objects.filter(
        user=request.user,
        status='completed',
        updated_at__gte=week_ago
    ).count()

    monthly_completion = Task.objects.filter(
        user=request.user,
        status='completed',
        updated_at__gte=month_ago
    ).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'todo_tasks': todo_tasks,
        'category_distribution': category_distribution,
        'weekly_completion': weekly_completion,
        'monthly_completion': monthly_completion,
    }

    return render(request, 'tasks/analytics.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    context = {
        'task': task,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_status = request.POST.get('status')
        if new_status in ['todo', 'in_progress', 'completed']:
            task.status = new_status
            if new_status == 'completed':
                task.completed_at = timezone.now()
            task.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def day_tasks(request, year, month, day):
    """View to display tasks for a specific day."""
    # Create a date object from the parameters
    selected_date = date(int(year), int(month), int(day))
    
    # Get tasks for the selected day
    tasks = Task.objects.filter(
        user=request.user,
        due_date=selected_date
    ).order_by('due_date')
    
    # Get categories for the filter
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'tasks': tasks,
        'categories': categories,
        'selected_date': selected_date,
    }
    
    return render(request, 'tasks/day_tasks.html', context) 