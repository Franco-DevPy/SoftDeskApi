from rest_framework import serializers
from .models import Issue
from projects.models import (
    Project,Contributor
)  # Importamos el modelo Project para usarlo en las validaciones
from .models import Comment



class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue

        # Campos que recibimos o mostramos en la API
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

        # Campos que NO puede modificar el usuario en POST/PUT
        read_only_fields = ["id", "created_at", "author"]

    # ✅ Se llama AUTOMÁTICAMENTE cuando creamos un Issue
    # Aquí asignamos el autor según el usuario autenticado
    def create(self, validated_data):
        # Tomamos el usuario desde la request
        user = self.context["request"].user

        # Forzamos a que `author` sea el usuario conectado
        validated_data["author"] = user

        return super().create(validated_data)

    # ✅ Validación personalizada para el assignee
    def validate_assignee(self, value):

        # Obtenemos el ID del proyecto desde la request
        project_id = self.initial_data.get("project")

        # Si no enviaron el proyecto, error
        if not project_id:
            raise serializers.ValidationError("Un projet doit être spécifié.")

        # Buscamos el proyecto en la base de datos
        project = Project.objects.filter(id=project_id).first()

        # Si el proyecto no existe
        if not project:
            raise serializers.ValidationError("Projet introuvable.")

        # Verificamos si el user asignado está en los contributors del proyecto
        # project.contributors es el related_name en el modelo Contributor
        if not project.contributors.filter(user=value).exists():
            raise serializers.ValidationError(
                "L'assigné doit être un contributeur au projet."
            )

        # Si todo está bien, devolvemos el valor
        return value


# 👇 NUEVO SERIALIZER COMMENT
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "created_at", "issue", "author"]
        read_only_fields = ["id", "created_at", "author"]

    def create(self, validated_data):
        # asignamos el autor automáticamente
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

    def validate_issue(self, value):
        # Comprobar que el usuario que comenta es contributor del proyecto del issue
        user = self.context["request"].user
        project = value.project


        if not Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                "Vous devez être contributeur du projet pour commenter cet issue."
            )

        return value
