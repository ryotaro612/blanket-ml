import csv
import google.cloud.bigquery as bq


def fetch_raw_events(output_filename: str):
    """ """
    client = bq.Client(location="us-east4")
    job = client.query(
        "select * from speeda-edge-prod.email.raw_sendgrid_event where timestamp > '2020-01-01'"
    )
    rows = job.result()
    with open(output_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['event_id', 'event', 'timestamp'])
        for row in rows:
            writer.writerow([field for field in row])

