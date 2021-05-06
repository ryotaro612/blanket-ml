import logging
import click
import dotenv
from . import email as em
from . import bigquery
from . import edge_web

dotenv.load_dotenv()

LOGGER = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True)
def main(verbose: bool):
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s:%(message)s")
    logging.getLogger(__name__).setLevel(logging.DEBUG if verbose else logging.INFO)


@main.group()
def email():
    pass


@email.command("raw")
@click.argument("output")
def fetch_email_raw_events(output: str):
    """ """
    client = bigquery.create_client()
    em.fetch_raw_events(client, output)


@email.command("format")
@click.argument("input")
@click.argument("output")
def format_raw_events(input: str, output: str):
    """ """
    em.format_raw_events(input, output)


@main.group()
def web():
    pass


@web.command("raw")
@click.argument("output")
def fetch_raw_requests(output: str):
    client = bigquery.create_client()
    edge_web.fetch_raw_events(client, output)
