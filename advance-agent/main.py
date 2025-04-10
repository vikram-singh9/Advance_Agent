import chainlit as cl
import os 
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional


load_dotenv()

#loaded environment variables from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-2.0-flash")


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token:str,
    raw_user_data: dict [str ,str],
    default_user: cl.User,


) -> Optional[cl.User]:
    """
    Handle the oauth callback from github
    return the user object if authentication is successful
    else return None

    """
    print(f"Provider: {provider_id}")
    print(f"User data: {raw_user_data}")

    return default_user

@cl.on_chat_start

async def handle_chat_start():

    cl.user_session.set("history", [])

    await cl.Message(content="Hello I am ChatBot build by Vikram! How can I help you 😎?").send()

@cl.on_message

async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})

    formated_history = []

    for msg in history:

        role = "user" if msg["role"] == "user" else "model"

        formated_history.append({"role":role, "parts": [{"text":msg["content"]}]})


    response = model.generate_content(formated_history)

    response_text = response.text if hasattr(response, "text") else ""

    history.append({"role" : "assistant", "content": response_text})

    cl.user_session.set("history", history)

    await cl.Message(content=response_text).send()


