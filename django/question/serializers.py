from rest_framework import serializers
from .models import Question, Option, Subject

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']

# question/serializers.py
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    subject = serializers.StringRelatedField()
    grade = serializers.CharField(source='get_grade_display')

    class Meta:
        model = Question
        fields = ['id', 'subject', 'grade', 'text', 'diagram', 'status', 'options', 'created_at']
