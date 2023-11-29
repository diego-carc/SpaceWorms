"""
Applies quantile normalization to a tabular data set obtained from merge_data.py
"""
# Import modules
import pandas as pd
import argparse

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to input file")
parser.add_argument("-o", "--output", help="Path to file to print output")
args = parser.parse_args()

# Read file
print("Reading file...")
data = pd.read_csv(args.input, sep='\t')

# Save original order
print("Indexing data...")
rank = {col : data[col].sort_values().index.to_list() for col in data.columns if col != "ProbeName"}

# Sort columns
sorted("Ranking data...")
sortedData = pd.DataFrame.from_dict({col : data[col].sort_values().to_list() for col in data.columns if col != "ProbeName"})

# Get mean across rows
print("Calculating mean..")
mean = sortedData.mean(axis=1)

# Re-order columns
print("Re order data...")
for col in data.columns:
    if col == "ProbeName": continue
    mean.index = rank[col]
    data[col] = mean.sort_index().to_list()

# Print output
print("Building output...")
data.to_csv(args.output, sep='\t', index=False)

print("Done!")