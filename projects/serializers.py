from rest_framework import serializers
from .models import Project, Contributor


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  
    class Meta:
        model = Project
        fields = ["id", "title", "type", "author"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "type", "author"]
        read_only_fields = ["id", "author"]  

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "role"]
