import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocess import clean_text

class ResumeScreener:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def rank_resumes(self, job_description, resumes):
        """
        Ranks resumes based on similarity to the job description.
        
        Args:
            job_description (str): The job description text.
            resumes (list of str): List of resume texts.
            
        Returns:
            list of float: Similarity scores corresponding to each resume.
        """
        if not resumes or not job_description:
            return []

        # 1. Preprocess
        clean_job = clean_text(job_description)
        clean_resumes = [clean_text(r) for r in resumes]

        # 2. Combine to form corpus for TF-IDF
        # The first element is the job description
        corpus = [clean_job] + clean_resumes

        # 3. Vectorize
        tfidf_matrix = self.vectorizer.fit_transform(corpus)

        # 4. Compute Cosine Similarity
        # distinct vectors: job_vector is index 0, resumes are 1..n
        job_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]

        # cosine_similarity returns a matrix (1 x n_resumes)
        similarities = cosine_similarity(job_vector, resume_vectors).flatten()

        return similarities.tolist()

    def get_missing_keywords(self, job_description, resume_text, top_n=10):
        """
        Identify high-value keywords from the job description that are missing or weak in the resume.
        """
        if not job_description or not resume_text:
            return []

        # 1. Preprocess
        clean_job = clean_text(job_description)
        clean_resume = clean_text(resume_text)

        # Common JD filler words to ignore
        ignored_words = {
            'experience', 'knowledge', 'understanding', 'looking', 'plus', 'must', 
            'year', 'years', 'working', 'work', 'strong', 'good', 'ability', 'skills',
            'job', 'role', 'team', 'candidate', 'proficiency', 'proficient'
        }

        # 2. Fit vectorizer on just these two docs
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([clean_job, clean_resume])
            feature_names = np.array(vectorizer.get_feature_names_out())

            # 3. Get vectors
            job_vector = tfidf_matrix[0].toarray().flatten()
            resume_vector = tfidf_matrix[1].toarray().flatten()

            # 4. Find terms with high score in Job but low/zero in Resume
            # Sort job indices by weight descending
            top_job_indices = job_vector.argsort()[::-1]
            
            missing_keywords = []
            for idx in top_job_indices:
                # Lower threshold to 0.05 or just rely on sorting. 
                # If many words are missing, individual weights drop due to normalization.
                if job_vector[idx] > 0.0:  
                    term = feature_names[idx]
                    # Check if totally missing and not in ignored list
                    if resume_vector[idx] == 0 and term not in ignored_words:
                        missing_keywords.append(term)
                    
                    if len(missing_keywords) >= top_n:
                        break
            
            return missing_keywords
        
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
