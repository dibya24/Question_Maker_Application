from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAdmin
from .models import Grade

class GradeCreateView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        name = request.data.get("name")
        grade = Grade.objects.create(name=name)
        return Response({"id": grade.id, "name": grade.name}, status=status.HTTP_201_CREATED)
