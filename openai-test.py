from openai import OpenAI
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


prompt = "Tell me a random fact"
response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant designed to output JSON",
        },
        {"role": "user", "content": prompt},
    ],
)


print(response.choices[0].message.content)
