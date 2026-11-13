import datetime
"""Organization B: reusable functions kept in one importable module."""
import csv
from collections import defaultdict
from pathlib import Path


def load(path):
    grouped=defaultdict(list)
    with open(path, encoding="utf-8", newline="") as f:
        for register,date,status in csv.reader(f): grouped[register].append((date,status))
    return grouped


def percentage(present, total):
    return 100 * present / total if total else 0.0


def compute(grouped):
    summary=[]; streaks=[]
    for register,rows in sorted(grouped.items()):
        present=sum(status=="P" for _,status in rows)
        summary.append((register,present,len(rows)-present,percentage(present,len(rows))))
        run=0; previous=None
        for date_text,status in sorted(rows):
            current=datetime.date.fromisoformat(date_text)
            consecutive=previous is not None and (current-previous).days==1
            run=(run+1 if consecutive else 1) if status=="A" else 0
            if run>=3: streaks.append(register); break
            previous=current
    return summary,streaks


def write(summary,streaks,out):
    out=Path(out); out.mkdir(exist_ok=True)
    with (out/"summary.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["register","present","absent","percentage"]); w.writerows(summary)
    (out/"three_day_absences.txt").write_text("\n".join(streaks)+("\n" if streaks else ""),encoding="utf-8")
