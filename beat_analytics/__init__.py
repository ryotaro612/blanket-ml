import logging
import click
import dotenv

dotenv.load_dotenv()

LOGGER = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True)
def main(verbose: bool):
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s:%(message)s")
    logging.getLogger(self.name).setLevel(
        logging.DEBUG if self.verbose else logging.INFO
    )


@main.command()
def fetch_email_events():
    raise RuntimeError()
