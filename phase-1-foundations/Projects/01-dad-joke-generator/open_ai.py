
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
topic = input("Enter a topic: ")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user", "content": f"Give me 5 dad jokes about {topic}"}]
)
print(response.choices[0].message.content)


# text = f"""
# You should express what you want a model to do by \
# providing instructions that are as clear and \
# specific as you can possibly make them. \
# This will guide the model towards the desired output, \
# and reduce the chances of receiving irrelevant \
# or incorrect responses. Don't confuse writing a \
# clear prompt with writing a short prompt. \
# In many cases, longer prompts provide more clarity \
# and context for the model, which can lead to \
# more detailed and relevant outputs.
# """
# prompt = f"""
# Summarize the text delimited by triple backticks \
# into a single sentence.
# ```{text}```
# """
# response = get_completion(prompt)
# print(response)