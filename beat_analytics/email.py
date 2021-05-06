import csv
import json
import os
import datetime
import jsonlines
import google.cloud.bigquery as bq
import beat_analytics.user as user


def fetch_raw_events(client: bq.Client, output_filename: str):
    """ """
    job = client.query(
        f"select * from {os.environ['RAW_EMAIL_TABLE']} where timestamp > '2020-01-01'"
    )
    rows = job.result()
    with open(output_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["event_id", "event", "timestamp"])
        for row in rows:
            writer.writerow([field for field in row])


def format_raw_events(input: str, output: str):
    """ """
    with open(input) as in_f, open(output, "w") as out_f:
        fieldnames = [
            "event_id",
            "event",
            "email",
            "event_timestamp",
            "ip",
            "sg_content_type",
            "sg_event_id",
            "sg_message_id",
            "sg_template_id",
            "sg_template_name",
            "useragent",
            "timestamp",
        ]
        writer = csv.DictWriter(out_f, fieldnames)
        writer.writeheader()
        for row in csv.DictReader(in_f):
            events = json.loads(row["event"])
            for event in events:
                writer.writerow(
                    {
                        "event_id": row["event_id"],
                        "event": event["event"],
                        "email": event["email"],
                        "event_timestamp": event["timestamp"],
                        "ip": event.get("ip", None),
                        "sg_content_type": event.get("sg_content_type", None),
                        "sg_event_id": event["sg_event_id"],
                        "sg_message_id": event["sg_message_id"],
                        "sg_template_id": event.get("sg_template_id", None),
                        "sg_template_name": event.get("sg_template_name", None),
                        "useragent": event.get("useragent", None),
                        "timestamp": row["timestamp"],
                    }
                )


def filter_link_events(events_file: str, output: str):
    with open(events_file) as in_f, open(output, "w") as out_f:
        fieldnames = [
            "event_id",
            "email",
            "ip",
            "sg_event_id",
            "sg_message_id",
            "sg_template_id",
            "sg_template_name",
            "event_timestamp",
            "url",
            "useragent",
            "timestamp",
        ]
        writer = csv.DictWriter(out_f, fieldnames)
        writer.writeheader()
        for row in csv.DictReader(in_f):
            events = json.loads(row["event"])
            for event in [event for event in events if event["event"] == "click"]:
                writer.writerow(
                    {
                        "event_id": row["event_id"],
                        "email": event["email"],
                        "ip": event.get("ip", None),
                        "sg_event_id": event["sg_event_id"],
                        "sg_message_id": event["sg_message_id"],
                        "sg_template_id": event.get("sg_template_id", None),
                        "sg_template_name": event.get("sg_template_name", None),
                        "event_timestamp": event["timestamp"],
                        "url": event["url"],
                        "useragent": event.get("useragent", None),
                        "timestamp": row["timestamp"],
                    }
                )


def load_event_file(filename: str):
    with open(filename) as f:
        result = []
        for record in csv.DictReader(f):
            record["timestamp"] = datetime.datetime.strptime(
                record["timestamp"], "%Y-%m-%d %H:%M:%S.%f%z"
            )
            result.append(record)
        return result


def filter_email_open_events(
    events_file: str, users_file: str, plans: dict, output: str
):
    events = load_event_file(events_file)
    open_events = [event for event in events if event["event"] == "open"]
    if len(open_events) == 0:
        return
    users = user.load_user_master(users_file)

    mail_user = dict((user["email"], user) for user in users)
    with open(output, "w") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(open_events[0].keys()) + ["user status"]
        )
        writer.writeheader()
        for event in open_events:
            plan_id = user.resolve_plan_id_by_email(
                event["email"], event["timestamp"], mail_user, plans
            )
            event["user status"] = plans.get(plan_id, "Free")
            writer.writerow(event)


def statistics_link_events(events_file: str, users_file: str, plans: dict, output: str):
    attach_user_status(events_file, users_file, plans, "click", output)


def attach_user_status(
    events_file: str, users_file: str, plans: dict, event_type: str, output: str
):
    events = load_event_file(events_file)
    if len(events) == 0:
        return
    users = user.load_user_master(users_file)
    mail_user = dict((user["email"], user) for user in users)
    with open(output, "w") as f:
        writer = csv.DictWriter(f, fieldnames=list(events[0].keys()) + ["user status"])
        writer.writeheader()
        for event in events:
            plan_id = user.resolve_plan_id_by_email(
                event["email"], event["timestamp"], mail_user, plans
            )
            event["user status"] = plans.get(plan_id, "Free")
            writer.writerow(event)
