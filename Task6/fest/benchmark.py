"""Set membership benchmark against linear duplicate scans."""
import statistics
import time


def set_unique(registers):
    seen=set(); unique=[]
    for reg in registers:
        if reg not in seen:
            seen.add(reg); unique.append(reg)
    return unique


def list_unique(registers):
    unique=[]; comparisons=0
    for reg in registers:
        found=False
        for prior in unique:
            comparisons += 1
            if prior == reg:
                found=True; break
        if not found: unique.append(reg)
    return unique, comparisons


def median_time(fn, values, repeats=3):
    times=[]
    for _ in range(repeats):
        start=time.perf_counter(); result=fn(values); times.append(time.perf_counter()-start)
    return statistics.median(times), result


def run_benchmarks():
    print("records,set_s,list_scan_s,comparisons,list_projection_s")
    pairwise_1000=None; comparisons_1000=0
    for n in (1_000,100_000):
        regs=[f"R{i:08d}" for i in range(n)]
        set_s, unique=median_time(set_unique,regs)
        if n==1_000:
            list_s,(list_result,comparisons)=median_time(list_unique,regs,repeats=1)
            pairwise_1000=list_s; comparisons_1000=comparisons
            projected=pairwise_1000*(n*(n-1)/2)/max(1,comparisons)
            assert len(unique)==len(list_result)
            print(f"{n},{set_s:.6f},{list_s:.6f},{comparisons},{projected:.4f}")
        else:
            all_pairs=n*(n-1)//2
            projected=pairwise_1000*all_pairs/max(1,comparisons_1000)
            print(f"{n},{set_s:.6f},not_run,{all_pairs},{projected:.1f}")
    print("100000 list scan is projected from the 1000-record measurement; not directly run.")
