#################################################
#                                               #
# AI ChatBot using OpenAI's GPT-3.5-turbo model #
#            Gradio inpliment                   #
#################################################

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio

# Load environment variables from a .env file (if present)
load_dotenv()

# Expect the OpenAI key to be in the environment variable `OPENAI_API_KEY`.
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError(
        "OpenAI API key not found. Please add `OPENAI_API_KEY` to a .env file or set the environment variable."
    )

client = OpenAI(api_key=api_key)
def create_response(user_input, state):

    # Ensure state is a list of message dicts
    if state is None:
        state = [{"role": "system", "content": "You are Pumpkin Py, a friendly and helpful python teacher"}]

    # Append user message and call the API
    state.append({"role": "user", "content": user_input})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=state
    )

    response = completion.choices[0].message.content
    state.append({"role": "assistant", "content": response})

    # Return both the visible text and the updated state for Gradio
    return response, state

# Use explicit components so we can control sizes and behavior
input_box = gradio.Textbox(label="Your question", placeholder="Type your question here...", lines=2, max_lines=50)
state_box = gradio.State()

response_box = gradio.Textbox(label="Pumpkin Py", lines=8, max_lines=400, interactive=False)

demo = gradio.Interface(fn=create_response,
                        inputs=[input_box, state_box],
                        outputs=[response_box, state_box],
                        title="Pumpkin Py ChatBot",
                        description="Ask Pumpkin Py, your friendly Python teacher, anything about Python programming!",
                        examples=[["What is a Python list?", [{"role": "system", "content": "You are Pumpkin Py, a friendly and helpful python teacher"}]]])

# Launch the Gradio demo
demo.launch()