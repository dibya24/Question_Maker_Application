# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from question.api import QuestionViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # <-- DRF API base
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
