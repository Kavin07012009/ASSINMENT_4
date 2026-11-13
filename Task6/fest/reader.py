"""Read and validate one department's registration CSV file."""
from pathlib import Path


class InvalidRegistration(ValueError):
    """Raised when a registration line is damaged or fails validation."""


def valid_email(email):
    email = email.strip()
    if email.count("@") != 1 or any(ch.isspace() for ch in email):
        return False
    local, domain = email.split("@")
    return bool(local and "." in domain and not domain.startswith(".") and not domain.endswith("."))


def parse_registration(line):
    fields = [field.strip() for field in line.rstrip("\r\n").split(",", 4)]
    if len(fields) != 5 or any(not fields[i] for i in range(4)):
        raise InvalidRegistration("expected register,name,department,email,events")
    register, name, department, email, event_text = fields
    if not valid_email(email):
        raise InvalidRegistration(f"invalid email {email!r}")
    events = {event.strip() for event in event_text.split(";") if event.strip()}
    if not events:
        raise InvalidRegistration("at least one event is required")
    return {"register": register, "name": name, "department": department,
            "email": email.lower(), "events": events}


def read_department(path):
    path = Path(path)
    records, errors = [], []
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                records.append(parse_registration(line))
            except InvalidRegistration as exc:
                errors.append((path.name, line_number, str(exc)))
    return records, errors
