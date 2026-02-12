from ml_engine.model import ResumeScreener

job_desc = """
We are looking for a Senior Python Developer with experience in Django and REST APIs.
Must have knowledge of Docker, AWS, and PostgreSQL.
Deep understanding of Machine Learning is a plus.
"""

resume_text = """
I am a Python Developer. I know Django and SQL.
I have worked on web applications.
"""

# Monkey patch/copy logic to debug
from ml_engine.preprocess import clean_text
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

print("--- DEBUGGING ---")
clean_job = clean_text(job_desc)
clean_resume = clean_text(resume_text)
print(f"Clean Job: {clean_job}")
print(f"Clean Resume: {clean_resume}")

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform([clean_job, clean_resume])
feature_names = np.array(vectorizer.get_feature_names_out())
job_vector = tfidf_matrix[0].toarray().flatten()

print("\n--- SCORES ---")
items = []
for idx, score in enumerate(job_vector):
    if score > 0:
        items.append((feature_names[idx], score))

# Sort by score desc
items.sort(key=lambda x: x[1], reverse=True)
for term, score in items:
    print(f"{term}: {score:.4f}")
