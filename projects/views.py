from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from .serializers import ContributorSerializer
from .models import Contributor


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
