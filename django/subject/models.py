from django.conf import settings
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # optional if you want to allow admin-less subjects
        blank=True
    )

    def __str__(self):
        return self.name
