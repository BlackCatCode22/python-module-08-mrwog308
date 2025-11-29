#################################################
#                                               #
# AI ChatBot using OpenAI's GPT-3.5-turbo model #
#                                               #
#################################################

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file (if present)
load_dotenv()

# Expect the OpenAI key to be in the environment variable `OPENAI_API_KEY`.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OpenAI API key not found. Please add `OPENAI_API_KEY` to a .env file or set the environment variable."
    )

client = OpenAI(api_key=api_key)

def create_response(user_input, messages):
    
    try:
        messages.append({"role": "user", "content": user_input})
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        return response
    except Exception as e:
        print("Oops, something went wrong:", e)
        return f"An error occurred: {str(e)}"
    
def main():
    messages = [
        {"role": "system", "content": "You are Pumpkin Py, a friendly and helpful python teacher"}
    ]
    print("Welcome to Pumpkin Py ChatBot! Type 'exit' to quit.\n")
    while True:
        user_input = input("Ask your Question: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = create_response(user_input, messages)
        print("Pumpkin Py says:", response)

if __name__ == "__main__":
    main()