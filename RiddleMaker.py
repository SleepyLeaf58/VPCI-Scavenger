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
            "content": "You are an AI assistant helping a game organizer create riddles to hide objects within a room. Given a description of the object and its location, generate a complex but solvable riddle (around 30 words). Focus on the object's features and uses while ensuring the clues are clear enough for players to find it with certainty. Mention the location subtly but accurately. Avoid being too vague—ensure all details lead players directly to the object without explicitly naming it."
        },

        {
            "role": "user",
            "content": UserDescription,
        }
    ],
    model="llama3-groq-70b-8192-tool-use-preview",
)

print(chat_completion.choices[0].message.content)
