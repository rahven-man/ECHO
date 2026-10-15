"""
profile_data.py
Streams each Yelp JSON Lines file and prints a profile:
row count, fields, null counts, value types, max string length, min/max of numbers.
Never loads a whole file into memory.
"""
import argparse
import json
import os
from collections import Counter, defaultdict
from tqdm import tqdm

RAW_DIR = os.path.join("data", "raw")
FILES = ["business", "review", "user", "checkin", "tip"]


def find_file(name):
    target = f"yelp_academic_dataset_{name}.json"
    for root, _, files in os.walk(RAW_DIR):
        if target in files:
            return os.path.join(root, target)
    raise FileNotFoundError(target)


def read_jsonl(path):
    """Generator: yields (record, bytes_in_line) one line at a time."""
    with open(path, "rb") as f:
        for line in f:
            yield json.loads(line), len(line)


def new_stats():
    return {"present": 0, "null": 0, "types": Counter(),
            "max_len": 0, "min": None, "max": None}


def profile(name, limit=None):
    path = find_file(name)
    total_bytes = os.path.getsize(path)
    stats = defaultdict(new_stats)
    rows = 0

    with tqdm(total=total_bytes, unit="B", unit_scale=True, desc=name) as pbar:
        for rec, nbytes in read_jsonl(path):
            rows += 1
            pbar.update(nbytes)
            for key, val in rec.items():
                s = stats[key]
                s["present"] += 1
                if val is None:
                    s["null"] += 1
                    continue
                s["types"][type(val).__name__] += 1
                if isinstance(val, str):
                    s["max_len"] = max(s["max_len"], len(val))
                elif isinstance(val, (int, float)) and not isinstance(val, bool):
                    s["min"] = val if s["min"] is None else min(s["min"], val)
                    s["max"] = val if s["max"] is None else max(s["max"], val)
            if limit and rows >= limit:
                break

    print(f"\n=== {name}: {rows:,} rows ===")
    print(f"{'field':<20}{'present':>10}{'null':>10}  {'types':<18}{'max_len':>8}  min / max")
    for key, s in stats.items():
        types = ",".join(s["types"])
        rng = f"{s['min']} / {s['max']}" if s["min"] is not None else ""
        print(f"{key:<20}{s['present']:>10,}{s['null']:>10,}  {types:<18}{s['max_len']:>8}  {rng}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="rows per file (quick test)")
    parser.add_argument("--files", nargs="*", default=FILES)
    args = parser.parse_args()
    for name in args.files:
        profile(name, args.limit)