from pathlib import Path
from reader import load
from stats import compute
from report import write

if __name__ == "__main__":
    base=Path(__file__).resolve().parents[1]
    summary,streaks=compute(load(base/"data"/"attendance.csv"))
    write(summary,streaks,Path(__file__).with_name("output"))
    print("three modules students/streaks:",len(summary),streaks)
