import csv
from collections import defaultdict

def load(path):
    grouped=defaultdict(list)
    with open(path,encoding="utf-8",newline="") as f:
        for register,date,status in csv.reader(f): grouped[register].append((date,status))
    return grouped
