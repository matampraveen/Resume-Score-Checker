# AI-Powered Resume Screening System - Walkthrough

This document outlines the features implementing, how to run the project, and the verification results.

## Implemented Features

### 1. Backend API (Django + DRF)
-   **Authentication**: JWT-based Signup/Login.
-   **Job Management**: Create, Read, Update, Delete Job Postings.
-   **Resume Handling**: Upload PDF/DOCX resumes, auto-extraction of text.
-   **Screening Engine**: TF-IDF & Cosine Similarity based ranking.

### 2. Frontend (Django Templates + Bootstrap)
-   **Dashboard**: Recruiter view to manage jobs.
-   **Job Detail**: View ranked candidates with similarity scores.
-   **Interactive**: JavaScript Fetch API for smooth interactions.

### 3. Database (MongoDB)
-   Connected via `djongo`.
-   Collections: `accounts_user`, `jobs_jobposting`, `resumes_resume`, `screening_screeningresult`.

## How to Run

### Prerequisites
-   Python 3.8+
-   MongoDB (Running locally on port 27017)

### Setup
1.  Isntall dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run Migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
3.  Start Server:
    ```bash
    python manage.py runserver
    ```

### Usage
-   **Frontend**: Navigate to `http://127.0.0.1:8000/`.
-   **API**: `http://127.0.0.1:8000/api/`
-   **Swagger Docs**: `http://127.0.0.1:8000/swagger/`

## Verification
A verification script `verify_api.py` is included to test the full flow programmatically.

Running `python verify_api.py` produced:
```
1. Registering User...
   User registered.
2. Logging in...
   Login successful.
3. Creating Job...
   Job created: Machine Learning Engineer (ID: 1)
4. Uploading Resume...
   Resume uploaded: Alice ML (ID: 1)
   Extracted Text: I am a Python developer with experience in Machine...
5. Screening Job 1...
   Screening triggered. Results count: 1
   - Alice ML: Score 0.3187840217537793
6. Fetching Results...
   Fetched 1 results.

All systems operational.
```
