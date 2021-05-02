import google.cloud.bigquery as bq


def create_client() -> bq.Client:
    client = bq.Client(location="us-east4")
    return client
