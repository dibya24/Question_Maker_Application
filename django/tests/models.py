from django.db import models
from question.models import Question  # import from your existing app

class Test(models.Model):
    title = models.CharField(max_length=255, default="Generated Test")
    questions = models.ManyToManyField(Question, related_name="tests")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
