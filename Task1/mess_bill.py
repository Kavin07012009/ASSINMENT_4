"""Repair for Task 1: stream mess-bill records and preserve rejected rows."""
from decimal import Decimal, InvalidOperation
from pathlib import Path


def total_mess_bill(filename, report_filename):
    total = Decimal("0.00")
    rejected = []
    with open(filename, "r", encoding="utf-8") as source, open(report_filename, "w", encoding="utf-8") as report:
        for line_number, raw in enumerate(source, start=1):
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            parts = [field.strip() for field in line.split(",")]
            if len(parts) != 3:
                rejected.append((line_number, line, "expected register,name,amount"))
                continue
            register, name, amount_text = parts
            try:
                amount = Decimal(amount_text)
                if not amount.is_finite() or amount < 0:
                    raise InvalidOperation
            except InvalidOperation:
                rejected.append((line_number, line, "invalid non-negative amount"))
                continue
            total += amount
            report.write(f"{register} {name} {amount:.2f}\n")
    return total, rejected


def main():
    sample = Path(__file__).with_name("mess_oct.txt")
    report_path = Path(__file__).with_name("report.txt")
    total, rejected = total_mess_bill(sample, report_path)
    print(report_path.read_text(encoding="utf-8"), end="")
    print(f"Total {total:.2f}")
    rejected_path = Path(__file__).with_name("rejected_lines.txt")
    rejected_path.write_text("\n".join(f"line {number}: {reason}: {raw}" for number, raw, reason in rejected) + ("\n" if rejected else ""), encoding="utf-8")
    print("Rejected:", rejected)


if __name__ == "__main__":
    main()
