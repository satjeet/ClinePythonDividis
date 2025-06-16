from rest_framework import serializers
from .models import WellnessSurveyAnswer, WellnessSurveySession

class WellnessSurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessSurveyAnswer
        fields = '__all__'

class WellnessSurveySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessSurveySession
        fields = '__all__'
