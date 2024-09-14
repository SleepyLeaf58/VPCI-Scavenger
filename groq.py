import os

from groq import Groq

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "give me a riddle based on the room location of an item on the first floor",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
