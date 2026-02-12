from django.urls import path
from .views import (
    IndexView, DashboardView, JobDetailView, JobCreateView, 
    ResumeUploadView, LoginView, RegisterView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('register/', RegisterView.as_view(), name='register_page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('jobs/create/', JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('resumes/upload/', ResumeUploadView.as_view(), name='resume_upload'),
]
