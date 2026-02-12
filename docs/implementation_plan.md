# Implementation Plan - AI-Powered Resume Screening System

This project is an AI-driven HR tool to automatically screen resumes against job descriptions using NLP and Machine Learning.

## User Review Required
> [!IMPORTANT]
> **Database**: We will use `djongo` to connect Django to MongoDB. Ensure a local MongoDB instance is running or provide a connection string.
> **ML Approach**: We will use a classic NLP approach (TF-IDF + Logistic Regression) as requested. For a "cold start" (no initial dataset), we will use pre-trained word embeddings or a synthetic dataset for the initial demo, or simply a cosine similarity baseline until feedback is gathered. **Decision**: I will implement a **Cosine Similarity** baseline using TF-IDF for the immediate "screening" feature without needing training data, and a placeholder for the Logistic Regression "Ranking" model that can be trained once data is collected.

## Proposed Changes

### Project Structure
```
resume_screener/
├── manage.py
├── resume_screener/      # Project config
├── apps/
│   ├── accounts/         # User auth & roles
│   ├── jobs/             # Job definitions
│   ├── resumes/          # Resume file handling
│   ├── screening/        # ML/Screening logic
│   └── analytics/        # Dashboard stats
├── ml_engine/            # NLP & ML core modules
│   ├── preprocess.py
│   ├── vectorizer.py
│   └── model.py
├── static/               # CSS/JS
└── templates/            # HTML
```

### 1. Backend & Database
- **Framework**: Django 4.x + Django REST Framework.
- **DB**: MongoDB via `djongo`.
- **Auth**: `Simple JWT`.

#### [NEW] `apps/accounts`
- Custom `User` model with `role` (recruiter, admin).

#### [NEW] `apps/jobs`
- `Job` model: title, description, required_skills (list), created_at.

#### [NEW] `apps/resumes`
- `Resume` model: candidate_name, file (FileField), parsed_text (TextField), uploaded_at.

#### [NEW] `apps/screening`
- `ScreeningResult` model: link to Job & Resume, score (float), recommended (bool).
- **Service**: `ScreeningService` to orchestrate parsing and scoring.

### 2. ML & NLP Pipeline (`ml_engine`)
- **Preprocessing**: Lowercase, remove stopwords (NLTK), lemmatize.
- **Vectorization**: `TfidfVectorizer` from `scikit-learn`.
- **Scoring**:
    1.  **Similarity**: Cosine similarity between Job Description vector and Resume vector.
    2.  **Keyword Match**: Explicit extraction of skills from Job Description and checking presence in Resume.

### 3. API
- `POST /api/auth/login/`
- `GET /api/jobs/`, `POST /api/jobs/`
- `POST /api/resumes/upload/` (Extracts text async or sync for MVP)
- `GET /api/screening/{job_id}/` (Returns ranked list)

### 4. Frontend
- **Tech**: Django Templates + Bootstrap 5.
- **Pages**:
    - Login / Signup
    - Recruiter Dashboard (List Jobs)
    - Job Detail (See screened candidates & scores)
    - Resume Upload (Drag & drop)

## Verification Plan

### Automated Tests
- Unit tests for `preprocess_text` function.
- Integration test for `Resume` upload api.

### Manual Verification
1.  Start MongoDB.
2.  Run Django server.
3.  Login as Recruiter.
4.  Post a Job "Python Developer".
5.  Upload 3 dummy resumes (1 relevant, 2 irrelevant).
6.  Verify the relevant one has a higher score in the dashboard.
