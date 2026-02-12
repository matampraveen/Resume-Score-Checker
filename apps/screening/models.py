from django.db import models
from apps.jobs.models import JobPosting
from apps.resumes.models import Resume

class ScreeningResult(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    score = models.FloatField() # Relevance score (0.0 to 1.0)
    skill_match_details = models.JSONField(default=dict) # E.g. {"matched": ["python"], "missing": ["java"]}
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.resume.candidate_name} for {self.job.title}: {self.score}"
