from typing import List
import re

def clean_text(text: str) -> str:
    """Clean the input text by removing unwanted characters and extra spaces."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading and trailing spaces
    return text

def tokenize_text(text: str) -> List[str]:
    """Tokenize the input text into words."""
    return text.split()  # Simple whitespace-based tokenization

def remove_stopwords(tokens: List[str], stopwords: set) -> List[str]:
    """Remove stopwords from the list of tokens."""
    return [token for token in tokens if token.lower() not in stopwords]

def preprocess_text(text: str, stopwords: set) -> List[str]:
    """Preprocess the input text: clean, tokenize, and remove stopwords."""
    cleaned_text = clean_text(text)
    tokens = tokenize_text(cleaned_text)
    return remove_stopwords(tokens, stopwords)