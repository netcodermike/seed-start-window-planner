from datetime import date, timedelta


def analyze(data):
    frost = date.fromisoformat(data["frostDate"])
    if frost.isoformat() != data["frostDate"]:
        raise ValueError("Use YYYY-MM-DD for the frost date")
    windows = []
    for crop in data["crops"]:
        name = crop["name"]
        low, high = crop["startBeforeDays"]
        after = crop["transplantAfterDays"]
        if not isinstance(name, str) or not name.strip() or any(type(days) is not int or not 0 <= days <= 365 for days in (low, high, after)):
            raise ValueError("Use a crop name and nonnegative offsets of up to 365 days")
        windows.append({"name": name.strip(), "start": (frost - timedelta(days=max(low, high))).isoformat(),
                        "end": (frost - timedelta(days=min(low, high))).isoformat(),
                        "transplant": (frost + timedelta(days=after)).isoformat()})
    return {"windows": sorted(windows, key=lambda entry: (entry["start"], entry["name"])), "frostDate": frost.isoformat()}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
