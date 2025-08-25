from django.db import models

class Difficulty(models.Model):
    level = models.CharField(max_length=50, unique=True)  # e.g. Easy, Medium, Hard
    description = models.TextField(blank=True)

    def __str__(self):
        return self.level
