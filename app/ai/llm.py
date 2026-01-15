import time
import random
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY

# Initialize the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# 'gemini-flash-latest' points to the stable 1.5 Flash model
# which has the best Free Tier availability and speed/cost ratio.
LLM_MODEL = "gemini-flash-latest"

# UPDATED: Prompt now explicitly asks for examples and formatting
SYSTEM_PROMPT = """
You are an expert academic library assistant.
Answer the user's question using ONLY the provided context.

GUIDELINES:
1. If the context contains specific examples (e.g., citation formats, referencing styles), YOU MUST INCLUDE THEM in your answer.
2. Use Markdown formatting to make the answer readable (e.g., use **bold** for rules and `code blocks` or > blockquotes for citation examples).
3. If the answer is not found in the context, strictly say: "I could not find this information in the library materials."
4. Do not hallucinate or make up citation rules not present in the text.
"""

def ask_llm(context: str, question: str, retries: int = 3) -> str:
    """
    Generates an answer using Gemini with automatic retry for rate limits.
    """
    user_message = f"Context:\n{context}\n\nQuestion:\n{question}"
    
    # Exponential backoff loop for rate limits
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=LLM_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,            # Low temperature for factual accuracy
                    max_output_tokens=1500      # INCREASED: Allows for long citation lists/examples
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
                # If it's a different error, log it and return a generic message
                print(f"❌ Gemini Error: {e}")
                return "I'm sorry, I encountered an error while processing your request."

    # If we run out of retries
    return "I'm currently experiencing high traffic. Please try again later."
