from rest_framework import viewsets
from .models import Difficulty
from .serializers import DifficultySerializer

class DifficultyViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer
