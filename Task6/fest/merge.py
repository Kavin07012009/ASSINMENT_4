"""Deduplicate by register number and combine selected events."""


def merge_registrations(records):
    master = {}
    duplicate_count = 0
    for record in records:
        key = record["register"].strip().casefold()
        if key in master:
            duplicate_count += 1
            master[key]["events"].update(record["events"])
            # Retain the first verified identity fields; fill a blank only if encountered.
            for field in ("name", "department", "email"):
                if not master[key][field] and record[field]:
                    master[key][field] = record[field]
        else:
            master[key] = {**record, "events": set(record["events"])}
    return master, duplicate_count
