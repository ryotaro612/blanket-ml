from google import genai
from google.genai import chats


def create_chat() -> chats.Chat:
    client = genai.Client()
    return client.chats.create(model="gemini-2.5-flash")
