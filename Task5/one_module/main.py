from pathlib import Path
from attendance_utils import load, compute, write

if __name__ == "__main__":
    base=Path(__file__).resolve().parents[1]
    summary,streaks=compute(load(base/"data"/"attendance.csv"))
    write(summary,streaks,Path(__file__).with_name("output"))
    print("one module students/streaks:",len(summary),streaks)
