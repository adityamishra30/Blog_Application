import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

if __name__ == "__main__":
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Write a 100-word blog about Django."
    )

    print(response.text)