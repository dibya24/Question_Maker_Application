# backend/question/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Option
from .serializers import QuestionSerializer, OptionSerializer
from rest_framework.permissions import IsAuthenticated

  # Create these serializers

# ----------------- Question CRUD -----------------

# List and Create Questions
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def question_list_create(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete a Question
@api_view(['GET', 'PUT', 'DELETE'])

def question_detail(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------- Option CRUD -----------------

# List and Create Options for a question
@api_view(['GET', 'POST'])
def option_list_create(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        options = Option.objects.filter(question=question)
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update, Delete an Option
@api_view(['GET', 'PUT', 'DELETE'])
def option_detail(request, id):
    try:
        option = Option.objects.get(id=id)
    except Option.DoesNotExist:
        return Response({"error": "Option not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OptionSerializer(option)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OptionSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
