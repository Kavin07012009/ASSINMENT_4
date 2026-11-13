"""Task 4: demonstrate defective overwrite logging and repaired append logging."""
from pathlib import Path


def bad_save_returns(books, filename):
    log = open(filename, "w", encoding="utf-8")
    for book in books:
        log.write(book)
    log.close()


def bad_process(day_file, filename):
    try:
        books = open(day_file, encoding="utf-8").read().split("\n")
        bad_save_returns([book for book in books if book], filename)
    except FileNotFoundError:
        print("missing")


def save_returns(books, filename, error_log):
    try:
        with open(filename, "a", encoding="utf-8") as log:
            for book in books:
                log.write(book + "\n")
    except (OSError, TypeError) as exc:
        with open(error_log, "a", encoding="utf-8") as errors:
            errors.write(f"write failure: {type(exc).__name__}: {exc}\n")
        raise


def process(day_file, filename, error_log):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = [line.strip() for line in source if line.strip()]
        save_returns(books, filename, error_log)
    except FileNotFoundError as exc:
        with open(error_log, "a", encoding="utf-8") as errors:
            errors.write(f"missing input {day_file}: {exc}\n")


def main():
    base = Path(__file__).parent
    input_dir, output_dir = base / "input", base / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    days = [input_dir / f"day{i}.txt" for i in range(1, 4)]
    bad_log = output_dir / "bad.log"
    bad_log.write_text("", encoding="utf-8")
    for day in days: bad_process(day, bad_log)
    print("Defective log (overwritten and concatenated):", repr(bad_log.read_text(encoding="utf-8")))
    try:
        bad_save_returns([object()], output_dir / "bad_failure.log")
    except TypeError as exc:
        print("Defective write failure was not logged:", type(exc).__name__, "error log exists:", (output_dir / "bad_errors.log").exists())
    fixed_log, errors = output_dir / "returns.log", output_dir / "errors.log"
    fixed_log.write_text("", encoding="utf-8"); errors.write_text("", encoding="utf-8")
    for day in days: process(day, fixed_log, errors)
    print("Repaired log:"); print(fixed_log.read_text(encoding="utf-8"), end="")
    process(input_dir / "missing.txt", fixed_log, errors)
    try:
        save_returns([object()], fixed_log, errors)
    except TypeError:
        print("write error logged:", errors.read_text(encoding="utf-8").strip().splitlines()[-1])


if __name__ == "__main__":
    main()
