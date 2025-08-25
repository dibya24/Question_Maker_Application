from rest_framework import serializers
from .models import Question, Option, Subject

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField(read_only=True)  # show subject name
    subject_id = serializers.PrimaryKeyRelatedField(          # accept subject_id when creating
        queryset=Subject.objects.all(),
        source="subject",
        write_only=True
    )
    options = OptionSerializer(many=True, required=False)     # allow posting options too
    grade_display = serializers.CharField(source="get_grade_display", read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "grade",          # stores raw value like "8"
            "grade_display",  # shows "Grade 8"
            "diagram",
            "status",
            "subject",
            "subject_id",
            "options",
            "created_at",
        ]

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question
