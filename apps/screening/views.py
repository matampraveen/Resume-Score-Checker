from rest_framework import views, viewsets, response, status, permissions, parsers
from .models import ScreeningResult
from .serializers import ScreeningResultSerializer
from apps.jobs.models import JobPosting
from apps.resumes.models import Resume
from ml_engine.model import ResumeScreener

class ScreeningView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        """
        Trigger screening for a specific job (pk).
        """
        try:
            job = JobPosting.objects.get(pk=pk)
        except JobPosting.DoesNotExist:
            return response.Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all resumes
        resumes = Resume.objects.all()
        if not resumes:
            return response.Response({"message": "No resumes found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare data for ML Engine
        resume_texts = [r.parsed_text for r in resumes]
        
        # Initialize Screener
        screener = ResumeScreener() # Should be instantiated once ideally, but ok for now
        
        # Rank
        scores = screener.rank_resumes(job.description + " " + job.required_skills, resume_texts)
        
        # Save results
        results = []
        for resume, score in zip(resumes, scores):
            # Upsert result
            result, created = ScreeningResult.objects.update_or_create(
                job=job,
                resume=resume,
                defaults={'score': score}
            )
            results.append(result)
        
        serializer = ScreeningResultSerializer(results, many=True)
        return response.Response(serializer.data)

class ScreeningResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get screening results for a job.
    """
    queryset = ScreeningResult.objects.all()
    serializer_class = ScreeningResultSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.request.query_params.get('job_id')
        if job_id:
            return self.queryset.filter(job__id=job_id)
        return self.queryset

import io
from pdfminer.high_level import extract_text
import docx

class InstantScreeningView(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        resume_file = request.FILES.get('resume')
        job_description = request.data.get('job_description')
        
        if not resume_file or not job_description:
            return response.Response(
                {"error": "Both 'resume' file and 'job_description' text are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract Text
        text = ""
        try:
            filename = resume_file.name.lower()
            if filename.endswith('.pdf'):
                text = extract_text(io.BytesIO(resume_file.read()))
            elif filename.endswith('.docx'):
                doc = docx.Document(io.BytesIO(resume_file.read()))
                text = " ".join([para.text for para in doc.paragraphs])
            elif filename.endswith('.txt'):
                text = resume_file.read().decode('utf-8')
            else:
                return response.Response(
                    {"error": "Unsupported file format. Use PDF, DOCX, or TXT."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
             return response.Response(
                {"error": f"Failed to read file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process with AI
        screener = ResumeScreener()
        # rank_resumes expects a list of resumes
        scores = screener.rank_resumes(job_description, [text])
        missing_keywords = screener.get_missing_keywords(job_description, text)
        
        score = scores[0] if scores else 0.0
        
        return response.Response({
            "score": score,
            "filename": resume_file.name,
            "missing_keywords": missing_keywords
        })
