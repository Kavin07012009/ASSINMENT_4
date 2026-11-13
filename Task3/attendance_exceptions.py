"""Task 3: complete TODO logic with custom exceptions and specific handlers."""
import os
import datetime
import tempfile
from pathlib import Path


class InvalidRecord(Exception):
    """Raised when a non-empty attendance row is malformed."""


class AttendanceFileError(Exception):
    """Raised when an attendance file cannot be read."""


def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, date, status = (part.strip() for part in parts)
    if not register or not date:
        raise InvalidRecord("register and date must be non-empty")
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    try:
        datetime.date.fromisoformat(date)
    except ValueError as exc:
        raise InvalidRecord(f"invalid date {date!r}") from exc
    return register, date, status


def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, start=1):
                if not line.strip():
                    continue
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_number, str(exc)))
                    continue
                if status == "P":
                    present += 1
                else:
                    absent += 1
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
        raise AttendanceFileError(f"cannot read {path}: {exc}") from exc
    else:
        return present, absent, errors
    finally:
        print(f"Finished reading attempt: {path}")


def broad_except_pass_demo():
    """Show how a typo is swallowed by the discouraged broad handler."""
    visible = "not set"
    try:
        attendence_total = 3
        visible = attendance_total  # intentional typo for this misuse demonstration
    except Exception:
        pass
    print("After broad except/pass, value is still:", visible)


def main():
    sample = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
              "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(sample); sample_path = tmp.name
    try:
        print("Expected complete-code result:", summarise(sample_path))
        try:
            summarise(Path(sample_path + ".missing"))
        except AttendanceFileError as exc:
            print("Missing file handled in summarise():", type(exc.__cause__).__name__)
        broad_except_pass_demo()
    finally:
        os.remove(sample_path)


if __name__ == "__main__":
    main()
