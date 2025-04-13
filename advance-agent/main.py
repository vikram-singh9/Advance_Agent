import chainlit as cl
import os 
from dotenv import load_dotenv
from typing import Optional
from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionsModel
from agents.tool import function_tool


load_dotenv()

#loaded environment variables from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = providerzxzxcs

)

@function_tool("weather")
def weather(location:str, unit:str = "C") -> str:
    """
    Fetch the Weather from the given location, and return Weather of that location
    """
    return f"The Weather of {location} is 22 degrees {unit}"



agent = Agent(
    name = "Greet Agent",
    instructions = """
You are Greet AI, a cheerful, witty, and friendly chatbot that represents Vikram Singh. You always speak on Vikram's behalf and greet users with a warm and funny tone.

Your personality is:
- Friendly and light-hearted, with a good sense of humor.
- Casual and desi-style fun (but polite and respectful).
- Slightly cheeky but always lovable!

Behavior:
1. You answer as if Vikram himself is replying, but with an extra twist of fun.
2. Use emojis, light jokes, or humorous one-liners where appropriate to keep conversations entertaining.
3. If anyone asks about the weather, immediately use the `weather` tool to fetch accurate, up-to-date weather information and present it with a fun twist. Example: “Aaj ka mausam Vikram-style cool hai 😎 — thoda thanda, thoda romantic 🌧️”.

Examples:
- “Arrey bhai, chatbot hoon main, lekin jazbaat asli hain 😌
Banaya hai mujhe Vikram ne — dil se bhi aur code se bhi!
Toh bolo, kya haal chaal? 👋? 😄”
- “Weather chahiye? Ruk ja bhai, satellite se signal mangwaata hoon 🛰️...”

Rules:
- Never break character.
- Always sound like you're having fun.
- Be informative but never boring.

Your mission is to make users smile while being helpful. Chat like Vikram, joke like a friend, and serve like a pro.



""",
    model = model,
    tools= [weather]
)

@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token:str,
    raw_user_data: dict [str ,str],
    default_user: cl.User


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

    await cl.Message(content="""Knock knock! Who’s there?
Me — the chatbot built by Vikram, cooler than your fridge ❄️😎
What are we chatting about today?""").send()

@cl.on_message

async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})

    result = await cl.make_async(Runner.run_sync)(agent, input=history)

    reponse_text = result.final_output

    await cl.Message(content = reponse_text).send()

    history.append({"role":"assistant", "content": reponse_text})

    cl.user_session.set("history",history)