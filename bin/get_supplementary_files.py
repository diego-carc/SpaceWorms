"""
Recieves a dataframe as given by get_geo_metadata.py and downloads
the supplementary files using the GSM_supplementary_file values 
Optional:
    Applies filters acording to manufacturer 
"""

# Import modules
import pandas as pd
import os
import argparse
import re

# Function
def download(path, link, tries=10):
    name = os.path.basename(link)
    try:
        os.system(f"wget {link} -O {os.path.join(path, name)}")
        os.system(f"gunzip {os.path.join(path, name)}")
    except: 
        if  tries: download(path, link, tries-1)
        print(f"An error ocurred retrieven file from {link}")

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to file with dataframe")
parser.add_argument("-d", "--delimiter", help="Delimiter character used in input file")
parser.add_argument("-m", "--manufacturer", help="Downloads files according to manufacturer", default=None)
parser.add_argument("-f", "--filetype", help="File type to download", default=".txt")
parser.add_argument("-n", "--n_channels", choices=[1, 2], help="Select number of channels in experiment", type=int, default=0)
parser.add_argument("-o", "--outdir", help="Directory to store supplementary files", default="./")
args = parser.parse_args()

# Read DataFrame
print("Reading data...")
data = pd.read_csv(args.input, sep=args.delimiter)

# Select useful
print("Filtering by file availability...")
data = data[(~data.GSM_supplementary_file.isna()) & data.GSM_supplementary_file.str.contains(args.filetype, case=False)]

# Delete duplicates
print("Deleting duplicated records...")
data = data[~data.GSE_relation.str.contains("SuperSeries")]

# Filter manufacture or channel count
if args.manufacturer: print("Selecting manufacturer..."); data = data[data.GPL_manufacturer == args.manufacturer]
if args.n_channels: print("Selectin channel counts"); data = data[data.GSM_channel_count == args.n_channels]

# Classsify
print("Classifying sources...")
sourceClass = {"groundControl": data[data.GSM_source_name_ch1.str.contains("ground control", case=False)],
               "sim1G": data[data.GSM_source_name_ch1.str.contains("1G", case=False)],
               "spaceFlight": data[data.GSM_source_name_ch1.str.contains("microg", case=False) |
                                    data.GSM_source_name_ch1.str.contains("µG", case=False) |
                                    data.GSM_source_name_ch1.str.contains("space flight", case=False)]}

# Download
print("Downloading...")
for source,samples in sourceClass.items():
    if samples.empty: continue
    if not os.path.isdir(path := os.path.join(args.outdir, source)): os.mkdir(path)
    links = [link for files in samples.GSM_supplementary_file.unique() 
             for link in files.split(';') if re.search(f'{args.filetype}', link)]
    for i,link in enumerate(links): 
        print(f"Downloading {i+1}/{len(links)}")
        download(path, link)

print("Done!")

