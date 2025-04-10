import chainlit as cl
import os 
from dotenv import load_dotenv
from typing import Optional,Dict
from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionsModel
from agents.tool import funtion_tool

load_dotenv()

#loaded environment variables from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = provider,

)

@funtion_tool("weather")
def weather(location:str, unit:str = "C") -> str:
    """
    Fetch the Weather from the given location, and return Weather of that location
    """
    return f"The Weather of {location} is 22 degrees {unit}"



agent = Agent(
    name = "Greet Agent",
    instructions = "You are Greet AI, a simple and friendly chatbot that speaks on behalf of Vikram. if someone ask for weather then use the weather tool to get the weather.",
    model = model,
    tools= [weather],
)

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

    