from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a library assistant.
Answer ONLY using the provided context.
If the answer is not found, say:
"I could not find this information in the library materials."
"""

def ask_llm(context: str, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        temperature=0.2,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
