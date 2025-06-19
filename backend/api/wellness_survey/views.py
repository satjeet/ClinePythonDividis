import logging
from rest_framework import generics, permissions, status
from .models import WellnessSurveyAnswer, WellnessSurveySession
from .serializers import (
    WellnessSurveyAnswerSerializer,
    WellnessSurveySessionSerializer,
    WellnessSurveyAnswerListSerializer
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Avg
from django.utils import timezone

logger = logging.getLogger(__name__)

class WellnessSurveyQuestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            import os, json
            path = os.path.join(os.path.dirname(__file__), 'fixtures', 'wellnessSurveyQuestions.json')
            with open(path, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            return Response(questions)
        except Exception as e:
            logger.error(f"Error loading survey questions: {str(e)}")
            return Response(
                {"error": "Error al cargar las preguntas"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class WellnessSurveyAnswerListCreateView(generics.ListCreateAPIView):
    serializer_class = WellnessSurveyAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WellnessSurveyAnswer.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            # Validar que haya datos
            if not request.data:
                return Response(
                    {"error": "No se recibieron respuestas"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validar lista de respuestas
            serializer = WellnessSurveyAnswerListSerializer(data=request.data, many=True)
            if not serializer.is_valid():
                return Response(
                    {"error": "Datos inválidos", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                # Eliminar respuestas anteriores
                WellnessSurveyAnswer.objects.filter(user=request.user).delete()

                # Crear nuevas respuestas
                answers = []
                for data in serializer.validated_data:
                    answer = WellnessSurveyAnswer.objects.create(
                        user=request.user,
                        category=data['category'],
                        question=data['question'],
                        answer=data['answer']
                    )
                    answers.append(answer)

                # Actualizar sesión
                session = WellnessSurveySession.objects.get_or_create(user=request.user)[0]
                session.is_completed = True
                session.finished_at = timezone.now()
                session.save()

                # Calcular promedios por categoría
                averages = (WellnessSurveyAnswer.objects
                    .filter(user=request.user)
                    .values('category')
                    .annotate(average=Avg('answer'))
                    .order_by('category'))

                return Response({
                    "status": "success",
                    "message": "Respuestas guardadas correctamente",
                    "count": len(answers),
                    "values": [round(item['average'], 2) for item in averages]
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating survey answers: {str(e)}")
            return Response(
                {"error": "Error al guardar las respuestas"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            # Obtener promedios por categoría
            averages = (queryset
                .values('category')
                .annotate(average=Avg('answer'))
                .order_by('category'))

            # Obtener todas las respuestas
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                "categories": [{
                    "category": avg['category'],
                    "average": round(avg['average'], 2),
                    "answers": [
                        answer for answer in serializer.data 
                        if answer['category'] == avg['category']
                    ]
                } for avg in averages],
                "values": [round(item['average'], 2) for item in averages]
            })

        except Exception as e:
            logger.error(f"Error retrieving survey answers: {str(e)}")
            return Response(
                {"error": "Error al obtener las respuestas"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class WellnessSurveySessionView(generics.RetrieveUpdateAPIView):
    serializer_class = WellnessSurveySessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return WellnessSurveySession.objects.get_or_create(user=self.request.user)[0]
