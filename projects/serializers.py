from rest_framework import serializers
from .models import Project
from .models import Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author"]
        read_only_fields = ["id", "author"]

    # asignamos el autor automáticamente al usuario autenticado
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        return super().create(validated_data)


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "role"]
