from datetime import datetime, timezone


def log(s):
    now = datetime.now(timezone.utc).astimezone().isoformat()
    print(f'{now} - {s}')