from django.urls import path, include
from rest_framework.routers import DefaultRouter
from question.api import QuestionViewSet
from student.views import StudentViewSet
from subject.views import SubjectViewSet
from difficulty.views import DifficultyViewSet
from tests.views import TestCreateView   # <- import your existing view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'difficulty', DifficultyViewSet, basename='difficulty')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/tests/create/', TestCreateView.as_view(), name='test-create'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
