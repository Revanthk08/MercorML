import pandas as pd
import re
import string
import nltk
import hnswlib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the dataset
df = pd.read_excel('dataset.xlsx')

# Preprocess the text data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text

# Apply preprocessing to the DESCRIPTION column
df['DESCRIPTION'] = df['DESCRIPTION'].apply(preprocess_text)

df['data'] = df['DESCRIPTION'] + ' ' + df['PRODUCT_NAME']

# Extract features using TF-IDF
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df['PRODUCT_NAME'])

# Convert sparse matrix to dense matrix
feature_vectors = feature_vectors.toarray()

# Build HNSW index
dim = feature_vectors.shape[1]
num_elements = feature_vectors.shape[0]
index = hnswlib.Index(space='cosine', dim=dim)
index.init_index(max_elements=num_elements, ef_construction=200, M=16)
index.add_items(feature_vectors, list(range(num_elements)))

# Function to suggest clothing based on input text
def suggest_clothing(input_text, num_suggestions=5):
    # Preprocess the input text
    text = preprocess_text(input_text)
    # Transform the input text into a feature vector using the same vectorizer
    input_vector = vectorizer.transform([text])
    input_vector = input_vector.toarray()

    # Perform approximate nearest neighbor search using HNSW
    labels, distances = index.knn_query(input_vector, k=num_suggestions)
    
    # Retrieve the URLs of the top-N suggestions
    suggestions = df.iloc[labels[0]]['URL'].tolist()
    
    return suggestions

# Example usage
input_text = input()
suggested_clothing = suggest_clothing(input_text, num_suggestions=5)
print("Top Suggested Clothing:")
for url in suggested_clothing:
    print(url)
