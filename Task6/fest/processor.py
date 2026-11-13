"""Coordinate department ingestion, resilient error capture and report writing."""
from pathlib import Path
from .reader import read_department
from .merge import merge_registrations
from .reports import write_outputs


def process_month(input_dir, output_dir, departments):
    input_dir = Path(input_dir)
    records, errors = [], []
    for department in departments:
        path = input_dir / f"{department}.csv"
        try:
            department_records, file_errors = read_department(path)
            records.extend(department_records); errors.extend(file_errors)
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
            errors.append((path.name, 0, f"{type(exc).__name__}: {exc}"))
            continue
    master, duplicates = merge_registrations(records)
    event_map = write_outputs(master, errors, output_dir)
    return master, duplicates, errors, event_map
