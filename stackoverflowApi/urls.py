from django.urls import path, include
from .views import  QuestionAPI, latest, QuestionCreateAPI, QuestionUpdateAPI

urlpatterns = [
    path('', QuestionAPI.as_view(), name="question_api"),
    path('create', QuestionCreateAPI.as_view(), name="question_create_api"),
    path('<int:id>', QuestionUpdateAPI.as_view(), name="question_update_api"),
    path('latest', latest, name="latest"),
]
