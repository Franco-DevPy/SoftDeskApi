from django.db import models
from django.conf import settings


class Project(models.Model):
    TYPE_CHOICES = [
        ("Back-end", "Back-end"),
        ("Front-end", "Front-end"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects_created",
    )

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributors"
    )
    role = models.CharField(
        max_length=20, choices=[("AUTHOR", "Author"), ("CONTRIBUTOR", "Contributor")]
    )

    class Meta:
        unique_together = ("user", "project")

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
