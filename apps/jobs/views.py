from rest_framework import viewsets
from .models import JobPosting
from .serializers import JobPostingSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    # permission_classes = [permissions.IsAuthenticated]
