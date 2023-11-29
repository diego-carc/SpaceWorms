"""
Makes a heatmap to compare expression of genes
The spaceFlight/groundControl ratio is transformed to log2
"""

# Import modules 
import pandas as pd
import seaborn as sns
import numpy as np
import argparse

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to file with normalized data")
parser.add_argument("-g", "--gpl", help="Path to file with GPL table")
parser.add_argument("-a", "--alpha", help="Value to cut differential expressed genes. The number of times expression doubles control. Def: 3", default=3, type=int)
parser.add_argument("-w", "--width", help="Width of the heatmap. Def: 8", default=8)
parser.add_argument("-e", "--height", help="Height of the heatmap. Def: 8", default=8)
parser.add_argument("-o", "--output", help="Path to file to save heatmap")
args = parser.parse_args()

# Read data
print("Reading data...")
data = pd.read_csv(args.input, sep='\t')
gpl = pd.read_csv(args.gpl, sep='\t')

# Delete control probes
print("Deleting control probes...")
data = data[(data.ProbeName != "DarkCorner") & (data.ProbeName != "GE_BrightCorner")]

# Extract annotated genes
print(f"Extracting annotated genes from {args.gpl}...")
genes = data.merge(gpl.loc[(gpl.GENE_NAME != "hypothetical protein") & (~gpl.GENE_NAME.isna()), ["ID", "GENE_NAME", "GB_ACC"]], left_on="ProbeName", right_on="ID")

# Get differentialy espressed genes
print("Calculating differential expression...")
sf_gc = np.log2(genes.spaceFlight / genes.groundControl)
a = args.alpha
crit = (sf_gc > a) | (sf_gc < -a)

# Plot heatmap
print("Making heatmap...")
sns.set(rc={'figure.figsize':(args.width, args.height)})
heatmap = sns.heatmap(genes.loc[crit, ["sim1G", "spaceFlight", "groundControl"]], yticklabels=genes.loc[crit, "GENE_NAME"])
fig = heatmap.get_figure()
fig.savefig(args.output,bbox_inches = 'tight')
print("Done!")