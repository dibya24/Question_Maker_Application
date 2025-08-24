from django.urls import path
from .api_views import QuestionListAPI

urlpatterns = [
    path('api/', QuestionListAPI.as_view(), name='question_api'),
]
