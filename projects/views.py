from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    ContributorSerializer,
)
from softdesk_api.permissions import (
    IsProjectAuthorOrReadOnly,
    IsProjectAuthorForContributors,
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributors__user=user).distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)

        Contributor.objects.get_or_create(
            user=self.request.user,
            project=project,
            role="AUTHOR",
        )


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthorForContributors]

    def get_queryset(self):
        user = self.request.user
        return Contributor.objects.filter(project__contributors__user=user).distinct()
