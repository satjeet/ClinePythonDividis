from rest_framework import generics, permissions
from .models import WellnessSurveyAnswer, WellnessSurveySession
from .serializers import WellnessSurveyAnswerSerializer, WellnessSurveySessionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class WellnessSurveyQuestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # Leer preguntas desde el JSON (ajustar ruta según despliegue)
        import os, json
        path = os.path.join(os.path.dirname(__file__), 'fixtures', 'wellnessSurveyQuestions.json')
        with open(path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        return Response(questions)

class WellnessSurveyAnswerListCreateView(generics.ListCreateAPIView):
    serializer_class = WellnessSurveyAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return WellnessSurveyAnswer.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WellnessSurveySessionView(generics.RetrieveUpdateAPIView):
    serializer_class = WellnessSurveySessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return WellnessSurveySession.objects.get_or_create(user=self.request.user)[0]
