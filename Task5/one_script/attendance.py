import datetime
"""Organization A: one self-contained script."""
import csv
from pathlib import Path
from collections import defaultdict


def percentage(present, total):
    return 100 * present / total if total else 0.0


def main():
    base = Path(__file__).resolve().parents[1]
    records = defaultdict(list)
    with (base / "data" / "attendance.csv").open(encoding="utf-8", newline="") as source:
        for register, date, status in csv.reader(source): records[register].append((date, status))
    summary, streaks = [], []
    for register, rows in sorted(records.items()):
        present = sum(status == "P" for _, status in rows)
        percent = percentage(present, len(rows))
        summary.append((register, present, len(rows) - present, percent))
        run = 0
        previous = None
        for date_text, status in sorted(rows):
            current = datetime.date.fromisoformat(date_text)
            consecutive = previous is not None and (current - previous).days == 1
            run = (run + 1 if consecutive else 1) if status == "A" else 0
            if run >= 3: streaks.append(register); break
            previous = current
    out = Path(__file__).with_name("output"); out.mkdir(exist_ok=True)
    with (out / "summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer=csv.writer(f); writer.writerow(["register","present","absent","percentage"]); writer.writerows(summary)
    (out / "three_day_absences.txt").write_text("\n".join(streaks)+("\n" if streaks else ""), encoding="utf-8")
    print("one script students/streaks:", len(summary), streaks)


if __name__ == "__main__": main()
