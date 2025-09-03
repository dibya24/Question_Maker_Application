from django.contrib import admin
from django.urls import path, include
from question import views as question_views
from student.views import StudentViewSet
from subject.views import SubjectViewSet
from difficulty.views import DifficultyViewSet
from tests.views import TestCreateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from grades.views import GradeViewSet   # ✅ import
from users.views import CustomTokenObtainPairView  # ✅ use custom token view

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'difficulty', DifficultyViewSet, basename='difficulty')
router.register(r'grades', GradeViewSet, basename='grade')  # ✅ add grades
# router.register(r'questions', question_views.QuestionViewSet, basename='question')¸   

urlpatterns = [
    # Question endpoints
    path("api/questions/", question_views.question_list_create, name="question-list-create"),
    path("api/questions/<int:id>/", question_views.question_detail, name="question-detail"),

    # Option endpoints
    path("api/questions/<int:question_id>/options/", question_views.option_list_create, name="option-list-create"),
    path("api/options/<int:id>/", question_views.option_detail, name="option-detail"),

    # Other registered routers
    path("api/", include(router.urls)),

    # Tests
    path("api/tests/create/", TestCreateView.as_view(), name="test-create"),

    # ✅ JWT auth with custom serializer
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # dj-rest-auth
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),

    # Django admin
    path("admin/", admin.site.urls),
]
