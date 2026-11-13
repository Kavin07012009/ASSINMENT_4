"""Write master, per-event participant, summary and error files."""
import csv
from pathlib import Path


def write_outputs(master, errors, output_dir):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "master.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out); writer.writerow(["register", "name", "department", "email", "events"])
        for key in sorted(master):
            item = master[key]
            writer.writerow([item["register"], item["name"], item["department"], item["email"], ";".join(sorted(item["events"]))])
    event_map = {}
    for item in master.values():
        for event in item["events"]:
            event_map.setdefault(event, []).append(item)
    for event, participants in event_map.items():
        safe_name = "".join(ch.lower() if ch.isalnum() else "_" for ch in event).strip("_")
        with (output_dir / f"event_{safe_name}.csv").open("w", encoding="utf-8", newline="") as out:
            writer=csv.writer(out); writer.writerow(["register", "name", "department", "email"])
            for person in sorted(participants, key=lambda p: p["register"]):
                writer.writerow([person["register"], person["name"], person["department"], person["email"]])
    with (output_dir / "summary.txt").open("w", encoding="utf-8") as out:
        out.write(f"unique registrations: {len(master)}\n")
        for event, participants in sorted(event_map.items()): out.write(f"{event}: {len(participants)}\n")
    with (output_dir / "errors.csv").open("w", encoding="utf-8", newline="") as out:
        writer=csv.writer(out); writer.writerow(["filename", "line_number", "reason"]); writer.writerows(errors)
    return event_map
