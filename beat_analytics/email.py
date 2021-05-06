import csv
import json
import os
import google.cloud.bigquery as bq


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
