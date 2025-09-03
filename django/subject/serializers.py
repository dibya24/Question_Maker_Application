from rest_framework import serializers
from .models import Subject
from question.models import Question, Option


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]  # add other fields if your Subject model has more
        

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    # use subject_id for input
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subject"
    )
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
            "subject_id",    # input field (integer ID)
            "subject_name",  # output field (string name)
            "options",
            "created_at",
        ]

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        question = Question.objects.create(**validated_data)

        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop("options", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if options_data is not None:
            instance.options.all().delete()
            for option_data in options_data:
                Option.objects.create(question=instance, **option_data)

        return instance
