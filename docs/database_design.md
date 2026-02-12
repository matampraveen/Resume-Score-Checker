# AI-Powered Resume Screening System - Database Design

## 1. Overview
The system uses **MongoDB** as the primary data store, interfaced via **Djongo** (a MongoDB connector for Django). This allows us to use Django's ORM while leveraging MongoDB's schema-less nature for unstructured data like resume text and screening results.

## 2. Collections & Schema

### 2.1 Users (`accounts_user`)
Stores user authentication and role details.
*   **Fields**:
    *   `_id` (ObjectId): Unique ID
    *   `username` (String): Unique username
    *   `password` (String): Hashed password
    *   `email` (String): User email
    *   `role` (String): 'admin' or 'recruiter'
    *   `date_joined` (Date)
*   **Sample Document**:
    ```json
    {
      "_id": ObjectId("65c1..."),
      "username": "recruiter_jane",
      "email": "jane@company.com",
      "role": "recruiter",
      "is_active": true,
      "date_joined": ISODate("2024-02-11T10:00:00Z")
    }
    ```

### 2.2 Job Postings (`jobs_jobposting`)
Stores job descriptions created by recruiters.
*   **Fields**:
    *   `_id` (ObjectId): Unique Job ID
    *   `title` (String): Job Title
    *   `description` (String): Full job description
    *   `required_skills` (String): Comma-separated skills
    *   `recruiter_id` (ObjectId): Reference to `accounts_user`
    *   `created_at` (Date)
*   **Sample Document**:
    ```json
    {
      "_id": ObjectId("65c2..."),
      "title": "Senior Python Developer",
      "description": "Looking for a Django expert...",
      "required_skills": "Python, Django, MongoDB",
      "recruiter_id": ObjectId("65c1..."),
      "created_at": ISODate("2024-02-11T12:00:00Z")
    }
    ```

### 2.3 Resumes (`resumes_resume`)
Stores metadata and parsed text of uploaded resumes.
*   **Fields**:
    *   `_id` (ObjectId): Unique Resume ID
    *   `candidate_name` (String): Name of candidate
    *   `file` (String): Path to file storage (media/resumes/...)
    *   `parsed_text` (String): **Large text field** containing extracted content
    *   `uploaded_at` (Date)
*   **Sample Document**:
    ```json
    {
      "_id": ObjectId("65c3..."),
      "candidate_name": "John Doe",
      "file": "resumes/john_doe.pdf",
      "parsed_text": "EXPERIENCE: Senior Dev... SKILLS: Python, SQL...",
      "uploaded_at": ISODate("2024-02-11T12:05:00Z")
    }
    ```

### 2.4 Screening Results (`screening_screeningresult`)
Stores the match score between a Job and a Resume.
*   **Fields**:
    *   `_id` (ObjectId): Unique Result ID
    *   `job_id` (ObjectId): Reference to `jobs_jobposting`
    *   `resume_id` (ObjectId): Reference to `resumes_resume`
    *   `score` (Float): Similarity score (0.0 - 1.0)
    *   `skill_match_details` (Object): JSON of matched/missing skills
*   **Sample Document**:
    ```json
    {
      "_id": ObjectId("65c4..."),
      "job_id": ObjectId("65c2..."),
      "resume_id": ObjectId("65c3..."),
      "score": 0.85,
      "skill_match_details": {
        "matched": ["Python", "Django"],
        "missing": ["MongoDB"]
      },
      "created_at": ISODate("2024-02-11T12:06:00Z")
    }
    ```

### 2.5 Audit Logs (`audit_logs`)
(Proposed) Tracks system usage for compliance.
*   **Sample Document**:
    ```json
    {
      "_id": ObjectId("65c5..."),
      "user_id": ObjectId("65c1..."),
      "action": "SCREEN_JOB",
      "target_id": ObjectId("65c2..."),
      "timestamp": ISODate("2024-02-11T12:06:00Z")
    }
    ```

## 3. Indexing Strategy
To ensure performance as data grows:
1.  **`users.username`**: Unique Index (Login performance)
2.  **`screening_results.job_id`**: Ascending Index (Fast filtering by job in dashboard)
3.  **`screening_results.score`**: Descending Index (Fast sorting of candidates)
4.  **`jobs.recruiter_id`**: Index (Filter jobs by recruiter)

## 4. Relationships & Django Interaction
*   **Djongo** translates Django Models (SQL-like) into MongoDB Documents.
*   **Foreign Keys**: Stored as `ObjectId` references. Django automatically handles the lookup (join-like behavior application-side or via aggregation).
*   **NoSQL Benefit**: The `parsed_text` field can be massive without affecting table schema performance. `skill_match_details` is stored as a flexible JSON object.

## 5. Scalability Considerations
*   **Sharding**: If `screening_results` grows largely, shard by `job_id` to keep all results for a job on one shard.
*   **Read/Write Split**: 
    *   **Heavy Writes**: Resume Text parsing (Async offload recommended).
    *   **Heavy Reads**: Dashboard querying screening results.
*   **Text Search**: For advanced search, we can enable MongoDB Atlas Search on `parsed_text`.
