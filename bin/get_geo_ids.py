'''
NAME
    get_geo_ids.py
  
VERSION
    1.0  28/11/2023


AUTHOR
    Diego Carmona Campos & Ethan Marcos Galindo Raya

DESCRIPTION
    Using Bio.Entrez, the script searches for GEO expression profiling by array GSEs related to 
    microgravity or space flight for a given taxid. Then, the accession numbers are saved in a 
    file. Optionally, the accession numbers can be formated in GEO accession IDs. 

USAGE

    % python get_geo_ids.py -e [Email to use in Bio.Entrez] -a [Apikey to use in Bio.Entrez (Optional)] 
    -t [Taxon ID of interest] -o [Path to file to print output] -m [Maximum number of records] -r [Max number of tries] 
    -f [Format accession numbers in GEO accession IDs]
    
ARGUMENTS
    --email: Email to use in Bio.Entrez
    --apikey: Apikey to use in Bio.Entrez (Optional)
    --taxid: Taxonid to search
    --outfile: Path to file to print output
    --max: Maximum number of records to retrieve with Entez.esearch
    --repeats: Number of times to try a query
    --format: Transform accession numbers to GEO accession IDs
'''

# Import modules
from Bio import Entrez
import argparse
from re import sub

# Functions
def format(accession: str):
    '''
    Converts an accession number to a GEO accession format
    Example: 200173985 -> GSE173985
    
    Args:
        accession(str): Accession number
    
    Returns:
        Accession number in a GEO accession format
    '''
    return(sub(r'^20*', 'GSE', accession))

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--email", help="Email to use in Entrez module")
parser.add_argument("-a", "--apikey", help="NCBI apikey to use in Entrez module (Optional)", required= False)
parser.add_argument("-t", "--taxid", help="Taxon id to search in [ORGN] field")
parser.add_argument("-o", "--outfile", help="Path to file to print output")
parser.add_argument("-m", "--max", help=f"Maximum number of records to retrive, default: {(temp:=1000)}", default=temp)
parser.add_argument("-r", "--repeats", help=f"Number of times to repeat a failed query. Default: {(temp:=10)}", default=temp, type=int)
parser.add_argument("-f", "--format", help="Wether to transform de accession number in a GEO accession format", action="store_true")
args = parser.parse_args()

# Init Entrez
Entrez.email = args.email
if args.apikey: Entrez.api_key = args.apikey

# Search term
print("Searching...")
tries = args.repeats
while tries:
    query = f'(((("microgravity" OR "Space flight") AND "txid{args.taxid}"[Organism]) AND "expression profiling by array"[DataSet Type]) AND "gse"[Entry Type]) '
    try:
        with Entrez.esearch(db="gds", term=query, retmax=args.max) as handle:
            record = Entrez.read(handle)['IdList']
            tries = 0
    except:
        print(f"Something went wrong. Repeats left: {tries}")
        tries -= 1

# Format
if args.format: print("Formating..."); record = [format(str(id)) for id in record]

# Print output
print("Building output...")
with open(args.outfile, 'w') as file:
    for id in record:
        file.write(f"{id}\n")

print("Done!")