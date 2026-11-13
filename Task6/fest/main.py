from pathlib import Path
from .processor import process_month
from .benchmark import run_benchmarks


def main():
    base=Path(__file__).resolve().parents[1]
    departments=["Arts","Science","Commerce","Engineering","Management"]
    master,duplicates,errors,event_map=process_month(base/"input",base/"output",departments)
    print("unique:",len(master),"duplicates merged:",duplicates)
    print("events:",{event:len(rows) for event,rows in sorted(event_map.items())})
    print("errors:",errors)
    for path in sorted((base/"output").iterdir()):
        print(f"--- {path.name} ---")
        print(path.read_text(encoding="utf-8").rstrip())
    run_benchmarks()


if __name__ == "__main__": main()
