# tests/serializers.py
from rest_framework import serializers
from .models import Test
from question.models import Question
# from question.api import QuestionSerializer
from question.serializers import QuestionSerializer

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_ids = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), many=True, write_only=True, source="questions"
    )

    class Meta:
        model = Test
        fields = ["id", "title", "questions", "question_ids", "created_at"]
