# AI-Powered Resume Screening System - API Documentation

## 1. Authentication Module

### 1.1 Register User
-   **Endpoint**: `/api/auth/register/`
-   **Method**: `POST`
-   **Auth Required**: No
-   **Description**: Registers a new user (recruiter or admin).
-   **Request Schema**:
    ```json
    {
        "username": "string (required)",
        "email": "string (email)",
        "password": "string (min 8 chars)",
        "role": "string ('recruiter' | 'admin')"
    }
    ```
-   **Response Schema (201 Created)**:
    ```json
    {
        "id": 1,
        "username": "user1",
        "email": "user1@test.com",
        "role": "recruiter"
    }
    ```
-   **Error Responses**:
    -   `400 Bad Request`: Username already exists or invalid data.
-   **Estimates**:
    -   Frequency: Low (Onboarding)
    -   Success Rate: 90%

### 1.2 Login
-   **Endpoint**: `/api/auth/login/`
-   **Method**: `POST`
-   **Auth Required**: No
-   **Description**: Authenticates user and returns JWT tokens.
-   **Request Schema**:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
-   **Response Schema (200 OK)**:
    ```json
    {
        "refresh": "eyJ0...",
        "access": "eyJ0..."
    }
    ```
-   **Estimates**:
    -   Frequency: High (Every session)
    -   Success Rate: 95%

---

## 2. Job Management Module

### 2.1 Create Job
-   **Endpoint**: `/api/jobs/`
-   **Method**: `POST`
-   **Auth Required**: Yes (Bearer Token)
-   **Request Schema**:
    ```json
    {
        "title": "Senior Python Dev",
        "description": "Full stack role...",
        "required_skills": "Python, Django, AWS"
    }
    ```
-   **Response Schema (201 Created)**:
    ```json
    {
        "id": 1,
        "title": "Senior Python Dev",
        ...
        "recruiter": 1,
        "created_at": "2024-02-11T..."
    }
    ```
-   **Handling Duplicates**: Duplicate titles are allowed; ID ensures uniqueness.

### 2.2 List Jobs
-   **Endpoint**: `/api/jobs/`
-   **Method**: `GET`
-   **Auth Required**: Yes
-   **Description**: Lists all jobs created by the logged-in recruiter.

---

## 3. Resume Module

### 3.1 Upload Resume
-   **Endpoint**: `/api/resumes/`
-   **Method**: `POST`
-   **Auth Required**: Yes
-   **Content-Type**: `multipart/form-data`
-   **Request Schema**:
    -   `candidate_name`: Text
    -   `file`: File (PDF/DOCX)
-   **Response Schema (201 Created)**:
    ```json
    {
        "id": 5,
        "candidate_name": "Alice",
        "parsed_text": "Extracted content..."
    }
    ```
-   **Error Responses**:
    -   `400`: Invalid file format.
    -   `500`: Extraction failure (Corrupt file).
-   **Estimates**:
    -   Frequency: Medium
    -   Success Rate: 98% (Failures mostly due to corrupted files)

---

## 4. Screening Module

### 4.1 Trigger Screening
-   **Endpoint**: `/api/screening/screen/{job_id}/`
-   **Method**: `POST`
-   **Auth Required**: Yes
-   **Description**: Triggers ML pipeline to rank all available resumes against the specific Job ID.
-   **Response Schema (200 OK)**:
    ```json
    [
        {
            "id": 1,
            "resume": { ... },
            "score": 0.85,
            "skill_match_details": {}
        },
        ...
    ]
    ```
-   **Performance**: Computationally heavy. 
-   **Estimates**:
    -   Frequency: Medium
    -   Success Rate: 99%

### 4.2 Get Results
-   **Endpoint**: `/api/screening/results/?job_id={id}`
-   **Method**: `GET`
-   **Auth Required**: Yes
-   **Description**: Retrieves stored screening results. Supports filtering.

---

## 5. Analytics Module (Integrated)
Analytics are currently embedded in the Screening Results. The `score` field allows for statistical analysis (e.g., finding the median quality of candidates).

-   **Future Endpoint**: `/api/analytics/stats/`
-   **Purpose**: Aggregated views (e.g., "Top 10 skills found in resumes").
