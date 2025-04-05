import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

from accounts.models import User
from tasks.models import Task, Category

# Get the superuser
user = User.objects.get(username='user1')

# Create some categories if they don't exist
categories = [
    'Work',
    'Personal',
    'Shopping',
    'Health',
    'Education',
    'Home',
    'Finance',
    'Travel',
    'Social',
    'Projects'
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)

# Sample task data
task_titles = [
    "Complete project proposal",
    "Schedule dentist appointment",
    "Buy groceries",
    "Review quarterly reports",
    "Plan weekend trip",
    "Update resume",
    "Call insurance company",
    "Clean garage",
    "Pay bills",
    "Research new laptop",
    "Book flight tickets",
    "Organize closet",
    "Schedule car maintenance",
    "Prepare presentation",
    "Send thank you notes",
    "Update software",
    "Plan birthday party",
    "File tax returns",
    "Buy birthday gift",
    "Schedule team meeting",
    "Review budget",
    "Clean windows",
    "Update portfolio",
    "Schedule doctor visit",
    "Plan dinner party",
    "Research vacation spots",
    "Organize files",
    "Schedule haircut",
    "Buy new shoes",
    "Plan workout routine"
]

descriptions = [
    "Need to complete this by end of week",
    "Important for health maintenance",
    "Get essentials for the week",
    "Review and analyze performance",
    "Plan activities and accommodation",
    "Update with latest achievements",
    "Discuss policy changes",
    "Spring cleaning task",
    "Pay all pending bills",
    "Compare different models",
    "Book for upcoming vacation",
    "Seasonal organization",
    "Regular maintenance check",
    "Prepare for client meeting",
    "Send to recent connections",
    "Update all applications",
    "Plan for next month",
    "Annual tax filing",
    "For upcoming birthday",
    "Weekly team sync",
    "Monthly financial review",
    "Spring cleaning task",
    "Add recent projects",
    "Annual checkup",
    "Host friends for dinner",
    "Research for summer vacation",
    "Digital organization",
    "Regular maintenance",
    "Replace old pair",
    "Create weekly schedule"
]

priorities = ['low', 'medium', 'high']
statuses = ['todo', 'in_progress', 'done']

# Create 30 tasks
for i in range(30):
    # Random date within next 30 days
    due_date = datetime.now() + timedelta(days=random.randint(1, 30))
    
    # Random completion date for some tasks
    completed_at = None
    if random.random() < 0.3:  # 30% chance of being completed
        completed_at = datetime.now() - timedelta(days=random.randint(1, 10))
    
    task = Task.objects.create(
        title=task_titles[i],
        description=descriptions[i],
        due_date=due_date,
        priority=random.choice(priorities),
        status=random.choice(statuses),
        user=user,
        category=Category.objects.get(name=random.choice(categories)),
        completed_at=completed_at
    )
    print(f"Created task: {task.title}")

print("Successfully created 30 sample tasks!") 