import time
import random
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

# 'gemini-flash-latest' automatically points to the best stable version (usually 1.5 Flash)
# This usually has better Free Tier availability than the specific 2.0 preview models.
LLM_MODEL = "gemini-flash-latest"

SYSTEM_PROMPT = """
You are a helpful library assistant.
Answer the user's question ONLY using the provided context below.
If the answer is not found in the context, strictly say:
"I could not find this information in the library materials."
Do not make up answers.
"""

def ask_llm(context: str, question: str, retries: int = 3) -> str:
    """
    Generates an answer using Gemini with automatic retry for rate limits.
    """
    user_message = f"Context:\n{context}\n\nQuestion:\n{question}"
    
    # Exponential backoff loop
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=LLM_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=500
                )
            )
            return response.text.strip()

        except Exception as e:
            error_str = str(e)
            
            # Check for Rate Limit (429) errors
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait_time = (2 ** attempt) + random.uniform(0, 1) # 1s, 2s, 4s...
                print(f"⚠️ Quota hit. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)
            else:
                # If it's not a rate limit error (e.g., 400 Bad Request), fail immediately
                print(f"❌ Gemini Error: {e}")
                return "I'm sorry, I encountered an error while processing your request."

    # If we run out of retries
    return "I'm currently experiencing high traffic. Please try again later."
