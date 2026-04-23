import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key = api_key)

def generate_movie_summary(title: str , director: str):
    model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type" : "application/json"})

    prompt = f"""you are a movie expert. Analyze '{title}' directed by {director}.
    return a JSON object with exactly two keys:
    - "summary": A one-sentence engaging summary.
    - "tags": A single string of 3 hash tags separated by commas (e.g., "#Action, #Thriller, #Nolan).
    """
    response = model.generate_content(prompt)

    ai_data = json.loads(response.text)
    return ai_data