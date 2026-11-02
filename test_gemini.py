import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=45000,                    
        retry_options=types.HttpRetryOptions(attempts=2),    # no silent retries
    ),
)

for model in ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]:
    start = time.time()
    try:
        interaction = client.interactions.create(
            model=model,
            system_instruction="You are a concise travel specialist.",
            input="3-day road trip from Columbus to Chicago. Max 12 lines.",
            generation_config={"thinking_level": "low"},
        )
        text = (interaction.output_text or "").strip()
        print(f"{model}: {time.time() - start:.1f}s, {len(text)} chars")
    except Exception as e:
        print(f"{model}: FAILED after {time.time() - start:.1f}s -> {e}")
