from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Issue, Comment
from .serializers import IssueSerializer, CommentSerializer

from projects.models import Contributor
from softdesk_api.permissions import (
    IsIssueAuthorOrProjectAuthorOrReadOnly,
    IsCommentAuthorOrProjectAuthorOrReadOnly,
)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueAuthorOrProjectAuthorOrReadOnly]

    def get_queryset(self):
    
        user = self.request.user
        project_ids = Contributor.objects.filter(user=user).values_list(
            "project_id", flat=True
        )
        return Issue.objects.filter(project_id__in=list(project_ids))

    def perform_create(self, serializer):
   
        user = self.request.user
        project = serializer.validated_data["project"]

        if not Contributor.objects.filter(user=user, project=project).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour créer un issue."
            )

        serializer.save(author=user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrProjectAuthorOrReadOnly]

    def get_queryset(self):

        user = self.request.user
        return Comment.objects.filter(
            issue__project__contributors__user=user
        ).distinct()

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)
