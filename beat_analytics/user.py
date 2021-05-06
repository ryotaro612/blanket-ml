import csv
import jsonlines


def user_master(
    user_file: str,
    user_plan_file: str,
    plan_file: str,
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
            "is_deleted": not "\\0" == user["is_deleted"],
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
        results[int(plan["id"])] = plan
    return results


def format_plan_histories(plan_histories):
    results = {}
    for history in plan_histories:
        user_id = int(history["user_id"])
        plans = results.get(user_id, [])
        plans.append(int(history["old_user_plan_id"]))
        results[user_id] = plans
    return results
