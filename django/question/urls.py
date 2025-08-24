from django.urls import path
from . import api_views  # this file should contain DRF API views

urlpatterns = [
    # Question API
    path('questions/', api_views.question_list_create_api, name='question_api'),           # GET, POST
    path('questions/<int:pk>/', api_views.question_detail_api, name='question_detail_api'), # GET, PUT, DELETE

    # Option API
    path('options/<int:question_id>/', api_views.option_list_create_api, name='option_api'),           # GET, POST
    path('options/<int:question_id>/<int:pk>/', api_views.option_detail_api, name='option_detail_api'), # GET, PUT, DELETE
]
