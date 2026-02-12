from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class IndexView(TemplateView):
    template_name = "web/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

class DashboardView(TemplateView):
    template_name = "web/dashboard.html"

class JobDetailView(TemplateView):
    template_name = "web/job_detail.html"

class JobCreateView(TemplateView):
    template_name = "web/job_create.html"

class ResumeUploadView(TemplateView):
    template_name = "web/resume_upload.html"

class LoginView(TemplateView):
    template_name = "web/login.html"

class RegisterView(TemplateView):
    template_name = "web/register.html"
