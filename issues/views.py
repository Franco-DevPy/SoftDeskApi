from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Issue
from .serializers import IssueSerializer
from projects.models import Contributor, Project
from .models import Comment
from .serializers import CommentSerializer


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    # 🔍 Mostrar SOLO issues de proyectos donde el usuario participa
    def get_queryset(self):
        user = self.request.user

        # Buscamos los proyectos donde el usuario es contributor
        project_ids = Contributor.objects.filter(user=user).values_list(
            "project_id", flat=True
        )

        # Retornamos los issues solo de esos proyectos
        return Issue.objects.filter(project_id__in=list(project_ids))

    # 🛠 Asignar automáticamente el autor del issue
    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data["project"]

        # ✅ Verificar que el user sea contributor del proyecto
        if not Contributor.objects.filter(user=user, project=project).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour créer un issue."
            )

        serializer.save(author=user)

    # ✏️ Controlar quién puede actualizar o borrar
    def perform_update(self, serializer):
        issue = self.get_object()
        user = self.request.user

        # Solo autor del issue o creador del proyecto puede editar
        if issue.author != user and issue.project.author != user:
            raise PermissionDenied(
                "Vous n'avez pas la permission de modifier cet issue."
            )

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.author != user and instance.project.author != user:
            raise PermissionDenied(
                "Vous n'avez pas la permission de supprimer cet issue."
            )

        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            issue__project__contributors__user=user
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
