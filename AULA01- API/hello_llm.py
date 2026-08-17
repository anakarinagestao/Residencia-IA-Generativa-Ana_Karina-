import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
api_key=os.getenv("OPENAI_API_KEY")
)

modelo = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

response = client.chat.completions.create(
model=modelo,

messages=[
{"role": "user", "content": "Qual a capital do Brasil?"}
],
)

print(response.choices[0].message.content)
