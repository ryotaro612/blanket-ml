import csv


def create_plan(master_file: str):
    with open(master_file) as f:
        result = {}
        for record in csv.DictReader(f, delimiter="\t"):
            result[int(record["id"])] = record["plan_name"]
        return result
