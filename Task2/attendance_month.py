"""Monthly attendance processor with per-file, per-line error reporting."""
import csv
import datetime
from pathlib import Path


def process_month(input_dir, output_dir):
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = {}
    errors = []
    files = sorted(input_dir.glob("*.csv"))
    for path in files:
        try:
            with path.open("r", encoding="utf-8", newline="") as source:
                for line_number, line in enumerate(source, start=1):
                    fields = [field.strip() for field in line.rstrip("\r\n").split(",")]
                    if len(fields) != 3 or not fields[0] or not fields[1] or fields[2] not in {"P", "A"}:
                        errors.append((path.name, line_number, "malformed attendance record"))
                        continue
                    register, date, status = fields
                    try:
                        datetime.date.fromisoformat(date)
                    except ValueError:
                        errors.append((path.name, line_number, "invalid date"))
                        continue
                    if register not in counts:
                        counts[register] = {"present": 0, "absent": 0}
                    counts[register]["present" if status == "P" else "absent"] += 1
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
            errors.append((path.name, 0, f"{type(exc).__name__}: {exc}"))
    with (output_dir / "attendance_percentages.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out); writer.writerow(["register", "present", "absent", "percentage"])
        for register, item in sorted(counts.items()):
            total = item["present"] + item["absent"]
            percent = 100 * item["present"] / total if total else 0.0
            writer.writerow([register, item["present"], item["absent"], f"{percent:.2f}"])
    with (output_dir / "below_75.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out); writer.writerow(["register", "percentage"])
        for register, item in sorted(counts.items()):
            total = item["present"] + item["absent"]
            percent = 100 * item["present"] / total if total else 0.0
            if percent < 75:
                writer.writerow([register, f"{percent:.2f}"])
    with (output_dir / "damaged_lines.csv").open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out); writer.writerow(["filename", "line_number", "reason"]); writer.writerows(errors)
    return counts, errors


def main():
    base = Path(__file__).parent
    counts, errors = process_month(base / "input", base / "output")
    print("Students:", len(counts), "damaged lines:", len(errors))
    for name in ("attendance_percentages.csv", "below_75.csv", "damaged_lines.csv"):
        path = base / "output" / name
        print(f"--- {name} ---")
        print(path.read_text(encoding="utf-8").rstrip())


if __name__ == "__main__":
    main()
