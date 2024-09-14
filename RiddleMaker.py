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
            "content":
"You are an AI assistant helping a game organizer create riddles to hide objects within a room. Given a description of the object and its location, generate a concise and specific riddle (around 20-25 words). Emphasize the object's distinctive features and its exact location, ensuring the riddle clearly directs players to the item. Make sure the clues are specific and unambiguous."
        },

        {
            "role": "user",
            "content": UserDescription,
        }
    ],
    model="llama3-groq-70b-8192-tool-use-preview",
)

print(chat_completion.choices[0].message.content)
