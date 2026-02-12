# AI-Powered Resume Screening System

## Prerequisites
-   Python 3.8+
-   MongoDB (Running locally on port 27017 or remote URI)

## Setup Instructions

1.  **Clone the Repository** (if not already done)
    ```bash
    git clone <repository_url>
    cd PROJECT-AI
    ```

2.  **Create Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migration**
    Apply the database schema (MongoDB collections).
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Superuser** (Optional, for admin access)
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

-   **Frontend**: Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
-   **API Documentation**: Open [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
-   **Admin Panel**: Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Testing

Run the verification script to test the full flow:
```bash
python verify_api.py
```
