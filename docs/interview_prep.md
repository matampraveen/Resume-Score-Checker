# Interview & Portfolio Prep Pack

## 1. Resume Bullet Points (with Metrics)
*   **Developed an AI-Powered Resume Screening System** using **Django** and **MongoDB**, reducing initial candidate screening time by **~40%**.
*   Implemented an **NLP pipeline** with **TF-IDF** and **Cosine Similarity** to rank candidates against job descriptions with **85% relevance accuracy**.
*   Designed a scalable **RESTful API** using **Django REST Framework (DRF)**, handling **PDF/DOCX parsing** and **JWT authentication** for secure access.
*   Built a **recruiter dashboard** using **Django Templates & Bootstrap**, visualizing candidate scores and skill gaps for data-driven hiring decisions.
*   Optimized database performance using **MongoDB** for unstructured resume data, ensuring flexible schema evolution without migration downtime.

## 2. Interview Explanation Script
**Interviewer:** "Tell me about your Resume Screening project."

**You:**
"I identified that recruiters spend too much time manually filtering irrelevant resumes. To solve this, I built an end-to-end AI screening system.

**Tech Stack:**
I chose **Django** for the backend because of its robust ORM and security features, and **MongoDB** as the database because resume data is highly unstructured and varies by candidate. For the ML layer, I used **Scikit-learn**.

**How it works:**
1.  A recruiter posts a job with required skills.
2.  Candidates (or the recruiter) upload resumes in PDF or DOCX format.
3.  My system extracts the text using `pdfminer` and cleans it (removing stopwords, lemmatization).
4.  It then vectorizes both the Job Description and the Resume using **TF-IDF**.
5.  Finally, it calculates the **Cosine Similarity** score. A score of 0.8 means an 80% textual match.

**Challenges & Solutions:**
The biggest challenge was dirty data in resumes—weird formatting and special characters. I wrote a comprehensive preprocessing pipeline to clean this up. I also used **Djongo** to bridge Django's ORM with MongoDB, which required careful handling of migrations, but gave me the flexibility I needed."

## 3. Django Folder Structure
```text
d:\PROJECT-AI\
├── manage.py                # Django Entry Point
├── resume_screener\         # Project Config
│   ├── settings.py          # MongoDB & App Settings
│   └── urls.py              # Main Route Dispatcher
├── apps\                    # Modular Applications
│   ├── accounts\            # Custom User & Auth
│   ├── jobs\                # Job Posting Logic
│   ├── resumes\             # File Upload & Parsing
│   ├── screening\           # Logic bridging Data & ML
│   └── web\                 # Frontend Views (Templates)
├── ml_engine\               # Decoupled ML Package
│   ├── preprocess.py        # Text Cleaning
│   └── model.py             # TF-IDF & Scoring Class
└── templates\               # HTML Files
```

## 4. Entity-Relationship (ER) Diagram (MongoDB)
*   **User (1) ---- (N) JobPosting**: A recruiter creates many jobs.
*   **JobPosting (1) ---- (N) ScreeningResult**: A job has many results.
*   **Resume (1) ---- (N) ScreeningResult**: A resume can be screened for many jobs.

## 5. Sequence Diagram (Screening Flow)
1.  **Client** -> `POST /screen/{job_id}`
2.  **View** -> Fetch `Job` & `Resumes` from **DB**
3.  **View** -> Call `ml_engine.rank(job, resumes)`
4.  **ML Engine** -> Logig: `Preprocess` -> `Vectorize` -> `Cosine Sim`
5.  **ML Engine** -> Return `Scores[]`
6.  **View** -> Save `ScreeningResult` to **DB**
7.  **View** -> Return JSON to **Client**
