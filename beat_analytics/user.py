import csv
import datetime
import jsonlines


def user_master(
    user_file: str,
    user_plan_file: str,
    plan_history_file: str,
    output: str,
):
    users = format_users(load_tsv(user_file))
    user_plans = format_user_plans(load_tsv(user_plan_file))
    plan_histories = format_plan_histories(load_tsv(plan_history_file))

    for user in users:
        plan_ids = plan_histories.get(user["user_id"], [])
        plan_ids.append(user["current_plan_id"])
        user["plans"] = [user_plans[plan_id] for plan_id in set(plan_ids)]
    with jsonlines.open(output, "w") as f:
        f.write_all(users)


def format_user(user: dict):
    return {"user_id": int(user["id"])}


def load_tsv(filename: str):
    with open(filename) as f:
        return [r for r in csv.DictReader(f, delimiter="\t")]


def format_users(users: [dict]):
    return [
        {
            "user_id": int(user["id"]),
            "created_date": user["created_date"],
            "is_deleted": transform_bool(user["is_deleted"]),
            "updated_date": user["updated_date"],
            "email": user["email"],
            "external_user_id": user["external_user_id"],
            "current_plan_id": int(user["current_plan_id"]),
        }
        for user in users
    ]


def format_user_plans(user_plans) -> dict:
    results = {}
    for plan in user_plans:
        user_plan_id = int(plan["id"])
        subscription_id = replace_null(plan["subscription_id"])
        results[user_plan_id] = {
            "user_plan_id": user_plan_id,
            "created_date": plan["created_date"],
            "cancel_date": replace_null(plan["cancel_date"]),
            "start_date": replace_null(plan["start_date"]),
            "end_date": replace_null(plan["end_date"]),
            "status": replace_null(plan["status"]),
            "subscription_id": subscription_id if subscription_id else None,
            "updated_date": plan["updated_date"],
            "paid": transform_bool(plan["paid"]),
            "plan_id": int(plan["plan_id"]),
        }
    return results


def format_plan_histories(plan_histories):
    results = {}
    for history in plan_histories:
        user_id = int(history["user_id"])
        plans = results.get(user_id, [])
        plans.append(int(history["old_user_plan_id"]))
        results[user_id] = plans
    return results


def load_user_master(filename: str):
    with jsonlines.open(filename) as users:
        result = []
        for user in users:
            plans = []
            for plan in user["plans"]:
                plan["start_date"] = parse_datetime(plan["start_date"])
                plan["cancel_date"] = parse_datetime(plan["cancel_date"])
                plan["end_date"] = parse_datetime(plan["end_date"])
                plans.append(plan)
            user["plans"] = plans
            result.append(user)
        return result


def transform_bool(sign: str):
    return not "\\0" == sign


def replace_null(value: str):
    return value if value != "NULL" else None


def resolve_plan_id_by_email(
    email: str, timestamp: datetime.datetime, email_user: dict, plans: dict
):
    if email not in email_user:
        return None
    for plan in email_user[email]["plans"]:
        start = plan["start_date"]
        end = plan["end_date"]
        cancel = plan["cancel_date"]
        if start <= timestamp and not end and not cancel:
            return plan["plan_id"]
        if start <= timestamp and (
            end and timestamp <= end or cancel and timestamp <= cancel
        ):
            return plan["plan_id"]
    return None


def parse_datetime(datetime_str):
    return (
        datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f").astimezone(
            datetime.timezone.utc
        )
        if datetime_str
        else None
    )
