from django import template

register = template.Library()

@register.filter
def filter_status(tasks, status):
    """
    Filter tasks by status
    """
    return [task for task in tasks if task.status == status]

@register.filter
def status_color(status):
    """
    Return Bootstrap color class for task status
    """
    colors = {
        'todo': 'secondary',
        'in_progress': 'warning',
        'done': 'success'
    }
    return colors.get(status, 'primary')

@register.filter
def priority_color(priority):
    """
    Return Bootstrap color class for task priority
    """
    colors = {
        'low': 'info',
        'medium': 'warning',
        'high': 'danger'
    }
    return colors.get(priority, 'primary') 