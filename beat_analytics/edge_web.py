import csv
import os
import google.cloud.bigquery as bq


def fetch_raw_events(client: bq.Client, output_filename: str):
    job = client.query(
        f"select request_id, request, timestamp from {os.environ['RAW_WEB_REQUEST_TABLE']} where timestamp > '2020-01-01'"
    )
    rows = job.result()
    with open(output_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["request_id", "request", "timestamp"])
        for row in rows:
            writer.writerow([field for field in row])