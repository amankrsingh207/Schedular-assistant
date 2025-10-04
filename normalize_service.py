import parsedatetime
from datetime import datetime
import pytz

TIMEZONE = 'Asia/Kolkata'

def normalize_entities(entities):
    cal = parsedatetime.Calendar()
    tz = pytz.timezone(TIMEZONE)

    date_phrase = entities.get('date_phrase', '').strip()
    time_phrase = entities.get('time_phrase', '').strip().upper()
    time_phrase = time_phrase.replace("AM", " AM").replace("PM", " PM").replace("  ", " ").strip()

    text = f"{date_phrase} {time_phrase}".strip()
    time_struct, parse_status = cal.parse(text)

    if parse_status == 0:
        return {"status": "needs_clarification", "message": "Could not normalize date/time"}

    dt = datetime(*time_struct[:6])
    if dt.tzinfo is None:
        dt = tz.localize(dt)

    return {
        "normalized": {
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H:%M"),
            "tz": TIMEZONE
        },
        "normalization_confidence": 0.95
    }
