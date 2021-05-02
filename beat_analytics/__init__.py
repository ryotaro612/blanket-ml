import logging
import click
import dotenv
from . import email as e
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
    e.fetch_raw_events(client, output)


@main.group()
def web():
    pass


@web.command("raw")
@click.argument("output")
def fetch_raw_requests(output: str):
    client = bigquery.create_client()
    edge_web.fetch_raw_events(client, output)
