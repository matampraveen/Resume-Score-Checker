import requests
import os

BASE_URL = "http://127.0.0.1:8000/api"
JOBS_URL = f"{BASE_URL}/jobs/"
RESUMES_URL = f"{BASE_URL}/resumes/"
SCREENING_URL = f"{BASE_URL}/screening/"

# No Authentication Header needed
headers = {}

# 1. Create Job
print("1. Creating Job...")
job_data = {
    "title": "Machine Learning Engineer",
    "description": "We need an ML expert with Python, Scikit-learn, and TensorFLow skills.",
    "required_skills": "Python, ML, Scikit-learn"
}
resp = requests.post(JOBS_URL, json=job_data, headers=headers)
if resp.status_code == 201:
    job = resp.json()
    job_id = job['id']
    print(f"   Job created: {job['title']} (ID: {job_id})")
else:
    print(f"   Job creation failed: {resp.status_code} {resp.text}")
    exit(1)

# 2. Upload Resume
print("2. Uploading Resume...")
# Generate a temporary file
with open("temp_resume.txt", "w") as f:
    f.write("I am a Python developer with experience in Machine Learning and Scikit-learn.")

files = {'file': ('resume.txt', open('temp_resume.txt', 'rb'))}
data = {'candidate_name': 'Alice ML'}
resp = requests.post(RESUMES_URL, files=files, data=data, headers=headers)
if resp.status_code == 201:
    resume = resp.json()
    print(f"   Resume uploaded: {resume['candidate_name']} (ID: {resume['id']})")
    print(f"   Extracted Text: {resume.get('parsed_text', '')[:50]}...")
else:
    print(f"   Resume upload failed: {resp.status_code} {resp.text}")
    exit(1)

# 3. Screen
print(f"3. Screening Job {job_id}...")
resp = requests.post(f"{SCREENING_URL}screen/{job_id}/", headers=headers)
if resp.status_code == 200:
    results = resp.json()
    print(f"   Screening triggered. Results count: {len(results)}")
    for res in results:
        print(f"   - {res['resume']['candidate_name']}: Score {res['score']}")
else:
    print(f"   Screening failed: {resp.status_code} {resp.text}")
    exit(1)

# 4. Check Results (GET)
print("4. Fetching Results...")
resp = requests.get(f"{SCREENING_URL}results/?job_id={job_id}", headers=headers)
if resp.status_code == 200:
    results = resp.json()
    print(f"   Fetched {len(results)} results.")
else:
    print(f"   Fetch results failed: {resp.status_code} {resp.text}")

print("\nAll systems operational (Authentication Removed).")
