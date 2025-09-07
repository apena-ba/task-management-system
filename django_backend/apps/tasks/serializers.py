from rest_framework import serializers
from apps.users.serializers import UserSerializer
from .models import (
    Task,
    Comment,
)


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(many=True, read_only=True)

    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task._meta.get_field("assigned_to").related_model.objects.all(),
        source="assigned_to",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "estimated_hours",
            "actual_hours",
            "created_by",
            "assigned_to",
            "assigned_to_ids",
            "tags",
            "parent_task",
            "metadata",
            "created_at",
            "updated_at",
            "is_archived",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class TaskAssignSerializer(serializers.Serializer):
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task._meta.get_field("assigned_to").related_model.objects.all(),
        write_only=True,
    )

    def update(self, instance, validated_data):
        users = validated_data.get("assigned_to_ids", [])
        for user in users:
            instance.assigned_to.add(user)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "task", "content", "created_by", "created_at"]
        read_only_fields = ["id", "task", "created_by", "created_at"]