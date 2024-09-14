import os

from groq import Groq

UserDescription = input()

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are and assistant for providing a riddle to help the organizer of the game hide an object. A description of a item or of a item's location inside a room will be given and you will create a complex but solvable riddle to help players find it. Around 30 words max and as specific as you can making it so the user can 100% find the answer without mentioning the object"
        },

        {
            "role": "user",
            "content": UserDescription,
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
