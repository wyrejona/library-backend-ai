import numpy as np
from google.generativeai import client as gclient
from app.config import GEMINI_API_KEY

# Configure Gemini client
gclient.configure(api_key=GEMINI_API_KEY)

def embed_text(text):
    """
    Generate embeddings using Google Gemini free API
    """
    # Call Gemini embeddings endpoint
    response = gclient.embeddings.create(
        model="gemini-text-embedding-3-large",  # free-tier embedding model
        text=text
    )
    
    # Convert to numpy array for FAISS
    return np.array(response['embedding'], dtype=np.float32)
