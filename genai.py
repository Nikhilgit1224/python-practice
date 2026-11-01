from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()
response = client.models.generate_content(model = "gemini-3.5-flash", contents ="give me a sample java code to print hello world")
print(response.text)