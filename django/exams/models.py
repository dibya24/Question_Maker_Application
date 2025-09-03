from django.db import models
from users.models import User

class Grade(models.Model):
    name = models.CharField(max_length=50)

class Subject(models.Model):
    name = models.CharField(max_length=50)

class DifficultyLevel(models.Model):
    level = models.CharField(max_length=50)

class Test(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "teacher"})
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE)

class Question(models.Model):
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)

class Submission(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    answers = models.JSONField()  # {question_id: "answer"}
    score = models.IntegerField(default=0)
