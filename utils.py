def build_final_json(entities, normalized):
    return {
        "appointment": {
            "department": entities.get("department", "Unknown").title(),
            "date": normalized.get("date", ""),
            "time": normalized.get("time", ""),
            "tz": normalized.get("tz", "")
        },
        "status": "ok"
    }
