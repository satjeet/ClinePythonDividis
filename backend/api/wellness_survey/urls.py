from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.WellnessSurveyQuestionsView.as_view(), name='wellness-survey-questions'),
    path('answers/', views.WellnessSurveyAnswerListCreateView.as_view(), name='wellness-survey-answers'),
    path('session/', views.WellnessSurveySessionView.as_view(), name='wellness-survey-session'),
]
