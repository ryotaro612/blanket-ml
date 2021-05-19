import logging
import click
import dotenv
from . import email as em
from . import bigquery
from . import edge_web
from . import user as us
from . import plan as p

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


@email.group()
def opening():
    pass


@opening.command("normalize")
@click.argument("input")
@click.argument("output")
def normalize_open_email(input: str, output: str):
    """ """
    em.normalize_open_email(input, output)


@opening.command("statistics")
@click.argument("events_file")
@click.argument("users_file")
@click.argument("plan_file")
@click.argument("output")
def statistics_open_email(
    events_file: str, users_file: str, plan_file: str, output: str
):
    plans = p.create_plan(plan_file)
    em.statistics_open_events(events_file, users_file, plans, output)


@email.group()
def link():
    pass


@link.command("normalize")
@click.argument("raw_email_events")
@click.argument("output")
def normalize_link_events(raw_email_events: str, output: str):
    em.filter_link_events(raw_email_events, output)


@link.command("statistics")
@click.argument("events_file")
@click.argument("users_file")
@click.argument("plan_file")
@click.argument("output")
def statistics_link_events(
    events_file: str, users_file: str, plan_file: str, output: str
):
    plans = p.create_plan(plan_file)
    em.statistics_link_events(events_file, users_file, plans, output)


@main.group()
def web():
    pass


@web.command("raw")
@click.argument("output")
def fetch_raw_requests(output: str):
    client = bigquery.create_client()
    edge_web.fetch_raw_events(client, output)


@main.group()
def user():
    pass


@user.command("master")
@click.argument("user")
@click.argument("user_plan")
@click.argument("plan_history")
@click.argument("output")
def user_master(user: str, user_plan: str, plan_history: str, output: str):
    us.user_master(user, user_plan, plan_history, output)
