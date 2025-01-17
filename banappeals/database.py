import os
from collections import OrderedDict

import dataset


def get() -> dataset.Database:
    return dataset.connect(f"sqlite:///{os.path.join('config', 'data.db')}")


def setup() -> None:
    db = get()
    applications = db.create_table("applications")
    applications.create_column("discord_user", db.types.text)
    applications.create_column("discord_id", db.types.bigint)
    applications.create_column("ban_reason", db.types.text)
    applications.create_column("ban_explanation", db.types.text)
    applications.create_column("unban_explanation", db.types.text)
    applications.create_column("additional_comments", db.types.text)
    applications.create_column("status", db.types.boolean)
    applications.create_column("reviewer", db.types.bigint)
    applications.create_column("timestamp", db.types.bigint)
    applications.create_column("ip_address", db.types.bigint)
    db.commit()
    db.close()


def check_if_app_exists(discord_id: int) -> bool:
    db = get()
    entry = db["applications"].find_one(discord_id=discord_id)
    db.close()
    return True if entry else False


def get_stats() -> dict:
    db = get()
    results = list(db.query("SELECT * from applications"))
    stats = {"pending": 0, "total": len(results), "accepted": 0, "rejected": 0}
    for row in results:
        if row["application_status"] is None:
            stats["pending"] += 1
        if row["application_status"]:
            stats["accepted"] += 1
        if not row["application_status"]:
            stats["rejected"] += 1
    return stats


def get_appeal(id: int = None, discord_id: int = None) -> OrderedDict:
    db = get()
    result = db["appeals"].find_one(id=id, discord_id=discord_id)
    db.close()
    return result


def get_appeals() -> OrderedDict:
    db = get()
    results = list(db.query("SELECT * from applications"))
    db.close()
    return results
