import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

openai = OpenAI(api_key=openai_api_key)
gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

system_prompt = "You are a helpful assistant. That responds in markdown without code blocks."

def stream_gpt(prompt):
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    stream = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages, stream=True)
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_gemini(prompt):
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    stream = gemini.chat.completions.create(model="gemini-2.5-flash", messages=messages, stream=True)
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_model(prompt, model):
    if model == "GPT":
        yield from stream_gpt(prompt)
    elif model == "Gemini":
        yield from stream_gemini(prompt)
    else:
        raise ValueError(f"Unknown model: {model}")

message_input = gr.Textbox(label="Your message:", info="Enter your message for GPT-4.1-mini", lines=7)
llm_dropdown = gr.Dropdown(label="Select LLM", choices=["GPT", "Gemini"], value="GPT")
message_output = gr.Markdown(label="Response: ")

view = gr.Interface(
    fn=stream_model,
    title="GPT Chat",
    inputs=[message_input, llm_dropdown],
    outputs=[message_output],
    examples=[
        ["Explain the Transformer architecture to a layperson.", "GPT"],
        ["Explain the Transformer architecture to an aspiring AI engineer.", "Gemini"],
    ],
    flagging_mode="never"
)

view.launch(inbrowser=True)
