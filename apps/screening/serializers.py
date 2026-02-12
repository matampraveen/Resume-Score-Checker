from rest_framework import serializers
from .models import ScreeningResult
from apps.resumes.serializers import ResumeSerializer

class ScreeningResultSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(read_only=True)
    
    class Meta:
        model = ScreeningResult
        fields = '__all__'
