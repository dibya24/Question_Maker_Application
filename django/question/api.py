# question/api.py
from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
from .models import Question, Option, Subject
from .serializers import QuestionSerializer

# ----------------- SERIALIZERS ------------------

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]


class QuestionReadSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    grade_display = serializers.CharField(source="get_grade_display", read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "grade",
            "grade_display",
            "diagram",
            "status",
            "subject",
            "options",
            "created_at",
        ]


class QuestionWriteSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subject"
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "grade",
            "diagram",
            "status",
            "subject_id",
            "options",
        ]

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop("options", None)
        instance = super().update(instance, validated_data)

        if options_data is not None:
            instance.options.all().delete()
            for option_data in options_data:
                Option.objects.create(question=instance, **option_data)
        return instance


# ----------------- VIEWSET ------------------

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]   # temporarily open (later switch to JWT)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return QuestionReadSerializer
        return QuestionWriteSerializer
