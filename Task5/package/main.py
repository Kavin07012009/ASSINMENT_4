from pathlib import Path
import attendance.stats
from attendance import stats
from attendance.stats import percentage
from attendance import load, compute, write

if __name__ == "__main__":
    base=Path(__file__).resolve().parents[1]
    summary,streaks=compute(load(base/"data"/"attendance.csv"))
    write(summary,streaks,Path(__file__).with_name("output"))
    print("package attendance students/streaks:",len(summary),streaks)
    print("import forms and percentage:", attendance.stats is stats, percentage(3, 4))
