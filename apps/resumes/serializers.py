from rest_framework import serializers
from .models import Resume
from .utils import extract_text_from_file

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('parsed_text', 'uploaded_at')

    def create(self, validated_data):
        resume = Resume.objects.create(**validated_data)
        
        # Auto-extract text
        if resume.file:
            try:
                # Provide full path for extraction
                text = extract_text_from_file(resume.file.path)
                resume.parsed_text = text
                resume.save()
            except Exception as e:
                # Log error but don't fail upload
                print(f"Extraction failed: {e}")
                
        return resume
