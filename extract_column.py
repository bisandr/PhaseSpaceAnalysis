# extract_column.py
#
# Loads a CSV file, extracts a single column by its number, and saves it as a new CSV file.
# The output file is named after the input file with the column number appended.
#
# Usage: python extract_column.py <input_file> <column_number> <output_dir>
#   input_file    — path to the input CSV file
#   column_number — 1-based index of the column to extract
#   output_dir    — directory where the output CSV file will be saved
#
# Example: python extract_column.py data/events5_260515.csv 3 output5/

import argparse
import csv
import os

parser = argparse.ArgumentParser(description="Extract a single column from a CSV file.")
parser.add_argument("input", help="Path to the input CSV file")
parser.add_argument("column", type=int, help="Column number to extract (1-based)")
parser.add_argument("output_dir", help="Directory to save the output CSV file")
args = parser.parse_args()

col_index = args.column - 1

rows = []
with open(args.input, newline="") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if col_index >= len(row):
            raise ValueError(f"Row {i + 1} has only {len(row)} columns, cannot extract column {args.column}.")
        rows.append([row[col_index]])

os.makedirs(args.output_dir, exist_ok=True)

input_stem = os.path.splitext(os.path.basename(args.input))[0]
output_path = os.path.join(args.output_dir, f"{input_stem}_col{args.column}.csv")

with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Extracted column {args.column} from {len(rows)} rows.")
print(f"Saved to {output_path}")
