from rest_framework import serializers
from .models import WellnessSurveyAnswer, WellnessSurveySession
from django.db import transaction

class WellnessSurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessSurveyAnswer
        fields = ['category', 'question', 'answer']
        read_only_fields = ['user']

    def validate_answer(self, value):
        """Validar que las respuestas estén en el rango correcto."""
        if not 0 <= value <= 10:
            raise serializers.ValidationError("La respuesta debe estar entre 0 y 10")
        return value

class WellnessSurveyAnswerListSerializer(serializers.Serializer):
    category = serializers.CharField(required=True, max_length=50)
    question = serializers.CharField(required=True, max_length=255)
    answer = serializers.IntegerField(required=True, min_value=0, max_value=10)

    def validate_answer(self, value):
        """Validar que las respuestas estén en el rango correcto."""
        if not 0 <= value <= 10:
            raise serializers.ValidationError("La respuesta debe estar entre 0 y 10")
        return value

    def validate(self, data):
        """Validar que la categoría y pregunta existan."""
        if not data.get('category'):
            raise serializers.ValidationError("La categoría es requerida")
        if not data.get('question'):
            raise serializers.ValidationError("La pregunta es requerida")
        return data

    def create(self, validated_data):
        return validated_data

    @classmethod
    def create_answers(cls, validated_data_list, user):
        """
        Crea o actualiza las respuestas de la encuesta para un usuario.
        Todas las operaciones se realizan en una única transacción.
        """
        answers = []
        with transaction.atomic():
            # Eliminar respuestas anteriores
            WellnessSurveyAnswer.objects.filter(user=user).delete()
            
            # Crear nuevas respuestas
            answers = []
            for data in validated_data_list:
                answer = WellnessSurveyAnswer.objects.create(
                    user=user,
                    category=data['category'],
                    question=data['question'],
                    answer=data['answer']
                )
                answers.append(answer)
            
            # Ordenar las respuestas por categoría para el radar chart
            answers.sort(key=lambda x: x.category)
            
        return answers

class WellnessSurveySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessSurveySession
        fields = ['current_step', 'is_completed', 'finished_at']
        read_only_fields = ['user']
