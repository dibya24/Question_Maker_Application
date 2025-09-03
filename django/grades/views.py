from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer
from .permissions import IsAdminOrReadOnly

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().order_by("name")
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
