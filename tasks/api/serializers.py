from rest_framework import serializers
from ..models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user']


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'priority',
            'status', 'category', 'category_name', 'owner', 'owner_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner'] 