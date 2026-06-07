# extract_series.py
#
# Reads a binary events CSV file and extracts time series for each of the 5 elements.
# For each row, it finds the 1-based positions of the 1s (one per element slot).
# It then computes the differences between consecutive elements within each row
# (2nd-1st, 3rd-2nd, etc.) and the sum of all four differences.
#
# Output files written to data/:
#   element_1st.csv ... element_5th.csv  — value series for each element position
#   diff_2nd-1st.csv ... diff_5th-4th.csv — difference series between adjacent elements
#   diff_sums.csv                         — sum of all four differences per row

import csv

input_path = "data/events.csv"

elements = [[] for _ in range(5)]

with open(input_path, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        indices = [i + 1 for i, val in enumerate(row) if val.strip() == "1"]
        for i in range(5):
            elements[i].append(indices[i])

diffs = [[elements[i + 1][j] - elements[i][j] for j in range(len(elements[0]))] for i in range(4)]
sums = [sum(diffs[i][j] for i in range(4)) for j in range(len(elements[0]))]

ordinals = ["1st", "2nd", "3rd", "4th", "5th"]
diff_labels = ["2nd-1st", "3rd-2nd", "4th-3rd", "5th-4th"]

for i, values in enumerate(elements):
    with open(f"data/element_{ordinals[i]}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([[v] for v in values])

for i, values in enumerate(diffs):
    with open(f"data/diff_{diff_labels[i]}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([[v] for v in values])

with open("data/diff_sums.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows([[v] for v in sums])

print("Files written:")
for ordinal in ordinals:
    print(f"  data/element_{ordinal}.csv")
for label in diff_labels:
    print(f"  data/diff_{label}.csv")
print("  data/diff_sums.csv")
