from google import genai

api_key = "YOUR GEMINI API KEY"

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is coding.",
)

print(response.text)
