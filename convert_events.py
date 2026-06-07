# convert_events.py
#
# Converts a binary-encoded events CSV file into an index-based CSV file.
# Each input row contains 0s and 1s representing whether an element is present.
# Each output row lists the 1-based positions (indices) of the 1s in that row.
#
# The output file is automatically named based on the number of indices per row
# and the date found in the input filename (e.g. events5_260515.csv).
#
# Usage: python convert_events.py [input_file]
#        Defaults to data/events.csv if no input file is provided.

import argparse
import csv
import os
import re

parser = argparse.ArgumentParser(description="Convert events CSV to index CSV.")
parser.add_argument("input", nargs="?", default="data/events.csv", help="Path to input CSV file (default: data/events.csv)")
args, _ = parser.parse_known_args()

input_path = args.input

result = []
with open(input_path, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        indices = [i + 1 for i, val in enumerate(row) if val.strip() == "1"]
        result.append(indices)

n_indices = len(result[0]) if result else 0
input_stem = os.path.splitext(os.path.basename(input_path))[0]
digits = re.findall(r"\d", input_stem)
date_suffix = "".join(digits[-6:]) if len(digits) >= 6 else "".join(digits)
output_path = f"data/events{n_indices}_{date_suffix}.csv"

with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(result)

print(f"Saved {len(result)} rows to {output_path}")
