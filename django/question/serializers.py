from rest_framework import serializers
from .models import Question, Option, Subject

# 🔹 Hardcoded subject list
SUBJECT_CHOICES = [
    "Math",
    "Science",
    "English",
    "Social",
    "Computer",
]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    # Write-only: accept subject string but only from hardcoded list
    subject = serializers.CharField(write_only=True, required=True)
    # Read-only: return the actual subject name from Subject model
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    options = OptionSerializer(many=True, required=False)
    grade_display = serializers.CharField(source="get_grade_display", read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "grade",
            "grade_display",
            "diagram",
            "status",
            "subject",       # write-only (string input)
            "subject_name",  # read-only (actual subject name)
            "options",
            "created_at",
        ]

    def validate_subject(self, value):
        """Ensure the subject is one of the allowed hardcoded subjects"""
        if value not in SUBJECT_CHOICES:
            raise serializers.ValidationError(
                f"Invalid subject. Allowed subjects: {', '.join(SUBJECT_CHOICES)}"
            )
        return value

    def create(self, validated_data):
        # Extract nested data
        options_data = validated_data.pop("options", [])
        subject_name = validated_data.pop("subject")

        # Ensure subject exists in DB
        subject_obj, _ = Subject.objects.get_or_create(name=subject_name)

        # Create question
        question = Question.objects.create(subject=subject_obj, **validated_data)

        # Create related options
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question

    def update(self, instance, validated_data):
        # Handle subject update if provided
        subject_name = validated_data.pop("subject", None)
        if subject_name:
            subject_obj, _ = Subject.objects.get_or_create(name=subject_name)
            instance.subject = subject_obj

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Handle options update
        options_data = validated_data.get("options")
        if options_data is not None:
            instance.options.all().delete()
            for option_data in options_data:
                Option.objects.create(question=instance, **option_data)

        return instance
