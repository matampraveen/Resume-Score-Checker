import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import os

# Download NLTK resources if not present
if os.environ.get('VERCEL'):
    nltk.data.path.append('/tmp')
    download_dir = '/tmp'
elif os.environ.get('RENDER'):
    # Render: Data should be in ./nltk_data (downloaded by build script)
    # We add it to path in settings.py, but good to be safe here too.
    nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))
    download_dir = os.path.join(os.getcwd(), 'nltk_data')
else:
    download_dir = None # Default local behavior

try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    print("NLTK data not found, downloading...")
    nltk.download('stopwords', download_dir=download_dir)
    nltk.download('wordnet', download_dir=download_dir)
    nltk.download('omw-1.4', download_dir=download_dir)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Cleans and preprocesses the Resume/Job description text.
    Steps:
    1. Lowercase
    2. Remove URLS
    3. Remove special chars and numbers
    4. Tokenize & remove stopwords
    5. Lemmatize
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove special characters and numbers (keep letters and spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize (split by space)
    tokens = text.split()
    
    # Remove stopwords and lemmatize
    cleaned_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words and len(word) > 2
    ]
    
    return " ".join(cleaned_tokens)
