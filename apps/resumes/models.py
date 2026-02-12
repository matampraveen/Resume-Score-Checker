from django.db import models

class Resume(models.Model):
    candidate_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    file = models.FileField(upload_to='resumes/')
    parsed_text = models.TextField(blank=True) # Text extracted from PDF/DOCX
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} - {self.uploaded_at}"
