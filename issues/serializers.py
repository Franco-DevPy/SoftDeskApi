from rest_framework import serializers
from .models import Issue
from projects.models import (
    Project,Contributor
)  # Importamos el modelo Project para usarlo en las validaciones
from .models import Comment



class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue

        fields = [
            "id",
            "title",
            "description",
            "tag",
            "status",
            "priority",
            "created_at",
            "project",
            "author",
            "assignee",
        ]

        read_only_fields = ["id", "created_at", "author"]


    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["author"] = user

        return super().create(validated_data)

    def validate_assignee(self, value):

        project_id = self.initial_data.get("project")

        if not project_id:
            raise serializers.ValidationError("Un projet doit être spécifié.")

        project = Project.objects.filter(id=project_id).first()

  
        if not project:
            raise serializers.ValidationError("Projet introuvable.")

      
        if not project.contributors.filter(user=value).exists():
            raise serializers.ValidationError(
                "L'assigné doit être un contributeur au projet."
            )

        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "created_at", "issue", "author"]
        read_only_fields = ["id", "created_at", "author"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def validate_issue(self, value):
        user = self.context["request"].user
        project = value.project


        if not Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                "Vous devez être contributeur du projet pour commenter cet issue."
            )

        return value
