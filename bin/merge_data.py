'''
NAME
    merge_data.py
  
VERSION
    1.0  28/11/2023


AUTHOR
    Diego Carmona Campos & Ethan Marcos Galindo Raya

DESCRIPTION
    Recieves a path to a directory containing the subdirectories created by get_supplementary_files.py.
    Iterates over all the .txt files, and parse asuming they are from Agilent Technologies. The script
    parse the files and calculate the mean over a set of observations (files in a subdirectory). Then, 
    the datasetes from the subdirectories is merged in a single file. 

USAGE

    % python merge_data.py -i [Path to directory used to store the ouput od get_supplementary_files] 
    -o [Path to file to print output]
    
ARGUMENTS
    --indir: Path to directory with subdirectories to merge data
    --output: Path to file to print output
'''

# Import modules
import pandas as pd
import os
import argparse

# Functions
def parseAgilent(file:str):
    """
    Parser to extract data from Agilent TXT files

    Args:
        file (str): Path to file with Agilent TXT data

    Returns
        Return a dataframe with the colums "ProbeName" and "gMeanSignal"
    """
    data = pd.read_csv(file, skiprows=range(9), sep='\t')
    data = data[["ProbeName", "gMeanSignal"]]
    return(data.set_index("ProbeName").squeeze())

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indir", help="Path to directory with subdirectories to merge data")
parser.add_argument("-o", "--output", help="Path to file to print output")
args = parser.parse_args()


# Merge data
matrix = []
for dir in os.listdir(args.indir):
    subdir = os.path.join(args.indir, dir)
    print(f"Parsing {subdir} files...")
    if not os.path.isdir(subdir): continue
    print("Parsing Agilent files...")
    tables = [parseAgilent(os.path.join(subdir,file)).rename(i) for i,file in enumerate(os.listdir(subdir))]
    matrix.append(pd.concat(tables, axis=1).mean(axis=1).rename(dir))

print("Building output...")
pd.concat(matrix, axis=1).to_csv(args.output, sep='\t')
print("Done!")

