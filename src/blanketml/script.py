import blanketml.model as m
from google.genai import chats
import blanketml.config as conf


def temp():

    config = conf.load("./config.toml")
    chat = m.create_chat()

    examples = []
    for post in config.posts.values():
        examples.append(
            {
                "ja": post.ja,
                "paper_path": post.paper,
            }
        )
    return m.fewshot(
        chat, "/home/ryotaro/Downloads/temp.pdf", examples, config.insutruction
    )
