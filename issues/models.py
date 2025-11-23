from django.db import models
from django.conf import settings
from projects.models import Project

# Create your models here.


class Issue(models.Model):
    TAG_CHOICES = [
        ("bug", "Bug"),
        ("feature", "Feature"),
        ("task", "Task"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("to do", "To Do"),
        ("in progress", "In Progress"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Un comentario pertenece a 1 Issue
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")

    # Quién escribió el comentario (un usuario)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.issue}"
