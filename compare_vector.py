# compare_vector.py
#
# Compares a new 5D integer vector against every row in a CSV data file.
# For each row, it counts how many elements of the new vector appear in that row.
# The script then prints a summary showing how many rows had 5, 4, 3, 2, or 1 matching elements.
#
# Usage: edit the 'new_vector' list below, then run the script.

import csv
from collections import Counter

DATA_FILE = "data/events5_260515.csv"

# --- Put your new vector here ---
new_vector = [7, 23, 37, 44, 47]
# --------------------------------

new_set = set(new_vector)

match_counts = Counter()

with open(DATA_FILE, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if not row:
            continue
        row_set = set(int(x) for x in row)
        matches = len(new_set & row_set)
        if matches > 0:
            match_counts[matches] += 1

print(f"New vector: {new_vector}\n")
print(f"{'Matches':<10} {'Count':>6}")
print("-" * 18)
for k in sorted(match_counts.keys(), reverse=True):
    print(f"{k} equal   {match_counts[k]:>6}")

total = sum(match_counts.values())
print("-" * 18)
print(f"Total rows with at least 1 match: {total}")
