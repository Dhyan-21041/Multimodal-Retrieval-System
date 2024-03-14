# -*- coding: utf-8 -*-
"""IR_Assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ZVVMVXmBBnXHmw8f4Nv__WorhytTuuy
"""

from google.colab import drive
drive.mount('/content/drive')

pip install pandas numpy nltk Pillow requests tensorflow

import pandas as pd
import numpy as np
import requests
import json
from io import BytesIO
from PIL import Image, ImageEnhance
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.models import Model
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import math
import pickle
from collections import defaultdict
from numpy.linalg import norm

# Ensure necessary NLTK datasets are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import os
from PIL import Image, ImageEnhance
import numpy as np
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import Model
import pickle
import pandas as pd

# Initialize the InceptionV3 model globally
inception_model = InceptionV3(weights='imagenet', include_top=False)
model = Model(inputs=inception_model.input, outputs=inception_model.output)

def preprocess_and_extract_features(image_url):
    """Preprocess an image from a URL and extract features using InceptionV3."""
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image = image.resize((299, 299))
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        image_array = np.array(image)
        image_array = preprocess_input(image_array)
        image_array = np.expand_dims(image_array, axis=0)
        features = model.predict(image_array)
        return (image_url, features.reshape(features.shape[0], -1).tolist())
    except Exception as e:
        print(f"Error processing image from URL {image_url}: {e}")
        return (image_url, None)

def preprocess_text(text):
    """Preprocess text data."""
    text = str(text).lower().translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(lemmatized_tokens)

def compute_tf(text):
    """Compute term frequency for a document."""
    tf_text = defaultdict(int)
    words = text.split()
    for word in words:
        tf_text[word] += 1
    return {word: count / len(words) for word, count in tf_text.items()}

def compute_idf(documents):
    """Compute inverse document frequency across a corpus."""
    idf_dict = defaultdict(int)
    N = len(documents)
    for document in documents:
        unique_words = set(document.split())
        for word in unique_words:
            idf_dict[word] += 1
    return {word: math.log(N / (count + 1)) for word, count in idf_dict.items()}

def compute_tfidf(documents):
    """Compute TF-IDF scores for all documents in a corpus."""
    idf_dict = compute_idf(documents)
    return [{word: tf * idf_dict[word] for word, tf in compute_tf(document).items()} for document in documents]

def save_data(data, file_name):
    """Serialize data to a file."""
    with open(file_name, 'wb') as file:
        pickle.dump(data, file)

if __name__ == "__main__":
    # Example DataFrame loading and processing
    df = pd.read_csv('/content/drive/MyDrive/IR_Assignments/Assignment_2/A2_Data.csv')
    df['Image'] = df['Image'].apply(lambda x: json.loads(x.replace("'", "\""))[0] if x else None)

    # Process images and text
    image_features_with_url = [preprocess_and_extract_features(url) for url in df['Image']]


    # Save the results
    save_data(image_features_with_url, '/content/drive/MyDrive/IR_Assignments/Assignment_2/image_features.pkl')

    composite_data = []

    for index, row in df.iterrows():
        image_url = row['Image']
        review_text = row['Review Text']

        # Process image and text
        image_features = preprocess_and_extract_features(image_url)
        preprocessed_review = preprocess_text(review_text)
        tfidf_scores = compute_tfidf([preprocessed_review])[0]

        composite_data.append({
            'image_url': image_url,
            'review_text': review_text,  # Save the main review text
            'preprocessed_review': preprocessed_review,
            'tfidf_score': tfidf_scores
        })

    save_data(composite_data, '/content/drive/MyDrive/IR_Assignments/Assignment_2/composite_data.pkl')

from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.models import Model
import requests
from PIL import Image, ImageEnhance
from io import BytesIO
import numpy as np
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import math

# Initialize InceptionV3 model globally to avoid reloading

inception_model = InceptionV3(weights='imagenet', include_top=False)
model = Model(inputs=inception_model.input, outputs=inception_model.output)

def preprocess_and_extract_features(image_url):
    """Preprocess an image from a URL and extract features using InceptionV3."""
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image = image.resize((299, 299)) # InceptionV3 requires input images to be 299x299 pixels
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        image_array = np.array(image)
        image_array = preprocess_input(image_array)
        image_array = np.expand_dims(image_array, axis=0)
        features = model.predict(image_array)
        # Normalize features
        features = features / np.linalg.norm(features)
        return (image_url, features.reshape(features.shape[0], -1).tolist())
    except Exception as e:
        print(f"Error processing image from URL {image_url}: {e}")
        return (image_url, None)

def preprocess_text(text):
    """Preprocess text data."""
    text = str(text).lower().translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(lemmatized_tokens)

def compute_tf(text):
    """Compute term frequency for a document."""
    tf_text = defaultdict(int)
    words = text.split()
    for word in words:
        tf_text[word] += 1
    return {word: count / len(words) for word, count in tf_text.items()}

def compute_idf(documents):
    """Compute inverse document frequency across a corpus."""
    idf_dict = defaultdict(int)
    N = len(documents)
    for document in documents:
        unique_words = set(document.split())
        for word in unique_words:
            idf_dict[word] += 1
    return {word: math.log(N / (count + 1)) for word, count in idf_dict.items()}

def compute_tfidf(documents):
    """Compute TF-IDF scores for all documents in a corpus."""
    idf_dict = compute_idf(documents)
    return [{word: tf * idf_dict[word] for word, tf in compute_tf(document).items()} for document in documents]

def cosine_similarity(features_a, features_b):
    """Compute cosine similarity for higher-dimensional numpy arrays."""
    # Flatten the features only for the purpose of dot product calculation
    features_a_flat = features_a.flatten()
    features_b_flat = features_b.flatten()

    # Ensure normalization
    features_a_norm = features_a_flat / np.linalg.norm(features_a_flat)
    features_b_norm = features_b_flat / np.linalg.norm(features_b_flat)

    dot_product = np.dot(features_a_norm, features_b_norm)
    return dot_product  # Since vectors are normalized, no need to divide by norms again


def cosine_similarity_text(vec_a, vec_b):
    """Compute cosine similarity for dictionaries (TF-IDF vectors)."""
    if isinstance(vec_a, dict) and isinstance(vec_b, dict):
        intersection = set(vec_a.keys()) & set(vec_b.keys())
        numerator = sum([vec_a[x] * vec_b[x] for x in intersection])
        sum1 = sum([val**2 for val in vec_a.values()])
        sum2 = sum([float(val)**2 for val in vec_b.values()])
        denominator = np.sqrt(sum1) * np.sqrt(sum2)
        return float(numerator) / denominator if denominator != 0 else 0.0
    else:
        raise ValueError("TF-IDF vectors must be of type dict.")

def find_most_similar(features_with_url, input_features, top_k=3):
    """Find the top k most similar items based on cosine similarity."""
    similarities = []
    for url, features in features_with_url:
        if features is not None:
            sim = cosine_similarity(input_features, np.array(features))
            similarities.append((url, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]

def find_most_similar_reviews(composite_data, input_tfidf, top_k=3):
    """Find and rank reviews based on text similarity."""
    similarities = []
    for item in composite_data:
        sim = cosine_similarity_text(input_tfidf, item['tfidf_score'])
        similarities.append((item['image_url'], sim, item['preprocessed_review']))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]

def save_results(filename, data):
    """Save data to a pickle file."""
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def main():
    # Prompt user for input
    image_url = input("Enter the image URL: ")
    review_text = input("Enter the review text: ")

    # Load pre-computed data
    with open('/content/drive/MyDrive/IR_Assignments/Assignment_2/image_features.pkl', 'rb') as file:
        image_features_with_url = pickle.load(file)
    with open('/content/drive/MyDrive/IR_Assignments/Assignment_2/composite_data.pkl', 'rb') as file:
        composite_data = pickle.load(file)

    # Preprocess and compute features for input image
    _, input_image_features = preprocess_and_extract_features(image_url)

    # Preprocess and compute TF-IDF for input review text
    input_review_tfidf = compute_tfidf([preprocess_text(review_text)])[0]

    # Find the top 3 similar images based on image features
    similar_images = find_most_similar(image_features_with_url, np.array(input_image_features), top_k=3)

    # Saving into pickled file
    save_results('/content/drive/MyDrive/IR_Assignments/Assignment_2/similar_images.pkl', similar_images)


    print("USING IMAGE RETRIEVAL")
    composite_results = []

    for (img_url, img_sim) in similar_images:
        # Find corresponding review in composite data and calculate text similarity
        review_data = next((item for item in composite_data if item['image_url'] == img_url), None)
        review_text = review_data['review_text'] if review_data else "Review not found"
        text_sim = cosine_similarity_text(input_review_tfidf, review_data['tfidf_score']) if review_data else 0

        # Calculate composite similarity score
        composite_similarity = (img_sim + text_sim) / 2

        # Append the results along with composite similarity score for sorting
        composite_results.append((img_url, review_text, img_sim, text_sim, composite_similarity))

    # Sort the results based on composite similarity score in descending order
    composite_results.sort(key=lambda x: x[4], reverse=True)

    # Print the sorted results
    for idx, (img_url, review_text, img_sim, text_sim, composite_similarity) in enumerate(composite_results, start=1):
        print(f"{idx}) Image URL: {img_url}\n Review: {review_text}\n Cosine similarity of images - {img_sim:.4f}\n Cosine similarity of text - {text_sim:.4f}\n Composite similarity score: {composite_similarity:.4f}\n")

    # Find the top 3 similar reviews based on text similarity
    similar_reviews = find_most_similar_reviews(composite_data, input_review_tfidf, top_k=3)

    # Saving into pickled file
    save_results('/content/drive/MyDrive/IR_Assignments/Assignment_2/similar_reviews.pkl', similar_reviews)


    print("USING TEXT RETRIEVAL")
    composite_results_text = []

    for (img_url, text_sim, review) in similar_reviews:
        # Find corresponding image feature similarity
        img_features = next((features for url, features in image_features_with_url if url == img_url), None)
        img_sim = cosine_similarity(np.array(input_image_features), np.array(img_features)) if img_features is not None else 0

        # Calculate composite similarity score
        composite_similarity = (img_sim + text_sim) / 2

        # Append the results along with composite similarity score for sorting
        composite_results_text.append((img_url, review, img_sim, text_sim, composite_similarity))

    # Sort the results based on composite similarity score in descending order
    composite_results_text.sort(key=lambda x: x[4], reverse=True)

    # Print the sorted results
    for idx, (img_url, review, img_sim, text_sim, composite_similarity) in enumerate(composite_results_text, start=1):
        print(f"{idx}) Image URL: {img_url}\n Review: {review}\n Cosine similarity of images - {img_sim:.4f}\n Cosine similarity of text - {text_sim:.4f}\n Composite similarity score: {composite_similarity:.4f}\n")


if __name__ == "__main__":
    main()

import pickle

def load_data(file_name):
    """Load serialized data from a file."""
    with open(file_name, 'rb') as file:
        return pickle.load(file)

# Specify the paths to your files
image_features_path = '/content/drive/MyDrive/IR_Assignments/Assignment_2/image_features.pkl'
similar_REVIEWS ='/content/drive/MyDrive/IR_Assignments/Assignment_2/similar_reviews.pkl'
similar_IMAGES ='/content/drive/MyDrive/IR_Assignments/Assignment_2/similar_images.pkl'



# Load the data
image_features = load_data(image_features_path)
images=load_data(similar_IMAGES)
review=load_data(similar_REVIEWS)

# Print the contents

print("Image Features (first item):", image_features[0][:10])  # Print first 10 features of the first item
print(review)
print(images)