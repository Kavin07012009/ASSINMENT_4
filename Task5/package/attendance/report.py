import csv
from pathlib import Path

def write(summary,streaks,out):
    out=Path(out); out.mkdir(exist_ok=True)
    with (out/"summary.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["register","present","absent","percentage"]); w.writerows(summary)
    (out/"three_day_absences.txt").write_text("\n".join(streaks)+("\n" if streaks else ""),encoding="utf-8")
