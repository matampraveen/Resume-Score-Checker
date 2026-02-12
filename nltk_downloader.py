import nltk
import os

# Set the path where NLTK data should be downloaded
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')

# Create the directory if it doesn't exist
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Add the path to NLTK data path
nltk.data.path.append(nltk_data_path)

print(f"Downloading NLTK data to {nltk_data_path}...")

# Download required NLTK data
nltk.download('stopwords', download_dir=nltk_data_path)
nltk.download('wordnet', download_dir=nltk_data_path)
nltk.download('omw-1.4', download_dir=nltk_data_path)

print("NLTK data download complete.")
