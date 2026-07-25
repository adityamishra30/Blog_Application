import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_article(title):
    prompt = f"""
    You are a professional blog writer.

    Write a detailed blog article on the topic:

    {title}

    Requirements:
    - Catchy title
    - Introduction
    - Use headings
    - Use bullet points where appropriate
    - Around 800-1000 words
    - Easy to understand
    - End with a conclusion
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text