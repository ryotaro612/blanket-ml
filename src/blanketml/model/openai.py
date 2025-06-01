""" """
import blanketml.config as conf
from openai import OpenAI


def _create_client() -> OpenAI:
    return OpenAI()


def _generate(client: OpenAI,  input: str | list[str], instructions: str | None, previous_response_id: str | None):
    """
    Note that Consider making instructions previous state mutually exclusive.
    """
    response = client.responses.create(
        model="gpt-4.1", input="Write a one-sentence bedtime story about a unicorn."
        instructions=instructions
        previous_response_id=previous_response_id
        
    )


def _encode_config(config: conf.Config) -> str:
    ...