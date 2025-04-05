from django import forms
from .models import Task, Category, TaskComment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'category', 'parent_task']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }


class TaskShareForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(is_superuser=True) 