from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsProjectAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request,  obj):
        
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsProjectAuthorForContributors(BasePermission):


    def has_permission(self, request, ):
        if request.method == "POST":
            project_id = request.data.get("project")
            if not project_id:
                return False
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                return False
            return project.author == request.user
        return True

    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.project.author == request.user


class IsIssueAuthorOrProjectAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request,  obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return obj.author == user or obj.project.author == user


class IsCommentAuthorOrProjectAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        project_author = obj.issue.project.author
        return obj.author == user or project_author == user
