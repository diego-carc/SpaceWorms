'''
NAME
    get_geo_metadata.py
  
VERSION
    1.0  28/11/2023


AUTHOR
    Diego Carmona Campos & Ethan Marcos Galindo Raya

DESCRIPTION
    The script recieves a file containing a list of GSEs accession numbers. Then, calls GEOparse 
    to download and parse GSE_familu.soft files to extract metadata. The metadata is stored in a
    tabular format.
    Optionally, the program also saves the GPL files.
    

USAGE

    % python get_geo_metadata.py -i [Path to file with GSMs list] -o [Path to file to print outpu] -g [Save GPL files] -r [Remove GSE_family.soft files]
    
ARGUMENTS
    --input: Path to file with GSEs lists
    --outfile: Path to file to print metadata in tabular format
    --gpl: Saves GPLs tables
    --remove: Delete GSE_familt.soft files
'''

# Import modules
import GEOparse
import pandas as pd
import argparse
import os

# Functions
def get_GEO(gse_id:str, path:str, i:int, m:int, delete:bool=False, tries:int=10):
    '''
    Calls GEOparse to parse GSE SOFT file and retrieve a GSE object

    Args:
        gse_id(str) : GEO accession id
        path(str): Path to dir to download SOFT file
        delete(bool): Wether to delete downloaded SOFT file
        tries(int): Number of tries before returning None
        i(int): Index to track the consult
        m(int): Total number of consults to do
    Return:
        GSE object or None
    '''
    print(f"Consulting {gse_id}: {i}/{m}")
    path = os.path.split(path)[0]
    try: 
        try: gse = GEOparse.get_GEO(geo=gse_id, path=path, silent=True); print("GEO parse succesful") 
        except: 
            print("Using ftp..")
            link = f'"ftp://ftp.ncbi.nlm.nih.gov/geo/series/{gse_id[:-3]}nnn/{gse_id}/soft/{gse_id}_family.soft.gz"'
            file = f"{gse_id}_family.soft.gz"
            print("Downloading...")
            os.system(f" wget {link} -O {os.path.join(path, file)}")
            print("Parsing...")
            gse = GEOparse.get_GEO(filepath=os.path.join(path, f"{gse_id}_family.soft.gz"), silent=True)
            print("Deleting...")
            os.remove(os.path.join(path, f"{gse_id}_family.soft.gz"))
    except: 
        if tries: return(get_GEO(gse_id, path, i, m, delete, tries-1))
        print(f"Error parsing {gse_id}") ; return(None)
    return(gse)

# Class
class gseMeta:
    """
    Class to organize GSE metadata
    """
    def __init__(self, GEO:GEOparse.GEOTypes.GSE) -> None:
        """
        Instances a gseMeta object
        
        Args:
            GEO: GEOparse.GEOTypes.GSE object to parse metadata
        """
        self.GEO = GEO

        self.meta = self.getMetadata(['geo_accession', 'type', 'relation'], "GSE")
        
        self.gsmsMeta = self.getMetadata(['geo_accession', 'type', 'source_name_ch1', 'channel_count','organism_ch1', 'taxid_ch1', 'characteristics_ch1',
                                           'platform_id','supplementary_file', 'series_id','source_name_ch2', 'organism_ch2', 'taxid_ch2', 'characteristics_ch2'], "GSM")
        
        self.gplsMeta = self.getMetadata([ 'geo_accession','technology', 'distribution', 'organism', 'taxid', 'manufacturer', "supplementary_file"], "GPL")
    
    def __mapKeys__(self, key:str, gtyp:str):
            """Helper to handle exception columns in self.getMetadata()"""
            if key == "geo_accession" : return(gtyp)
            if key == "series_id" : return("GSE")
            if key == "platform_id" : return("GPL")

    def __mapVals__(self, val:str, geo:str):
            """Helper to handle exception columns in self.getMetadata()"""
            if val == "geo_accession" : return(geo.name)
            if val == "series_id" : return(self.GEO.name)
            if val == "platform_id" : return(';'.join(geo.metadata.get("platform_id", ["None"])))
    
    def getMetadata(self, columns, gtyp):
        """Makes a dataframe with the metadata indicated in columns for de GEO of type gtyp"""
        if gtyp == "GSM": values = self.GEO.gsms.values()
        elif gtyp == "GPL": values = self.GEO.gpls.values()
        else: values = [self.GEO]
        exceptions = ["geo_accession", "series_id", "platform_id"]


        meta = [{f"{gtyp}_{c}" if c not in exceptions  else self.__mapKeys__(c, gtyp) : ';'.join(geo.metadata.get(c,["None"])) if c not in exceptions else self.__mapVals__(c,geo) 
                 for c in columns} for geo in values]   
         
        return(pd.DataFrame.from_dict(meta))
    
    def getAllMeta(self):
         return(pd.merge(self.meta, self.gsmsMeta).merge(self.gplsMeta))
    
# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input",help="Path to input file containing a list of GSEs GEO accession ids")
parser.add_argument("-o", "--outfile", help="Path to file to print output file")
parser.add_argument("-g", "--gpl", help="Wheter to save GPL table. Default: True", action="store_true")
parser.add_argument("-r", "--remove", help="Wether to remove GSE_family.soft.files", action="store_true")
args = parser.parse_args()

# Read GSE accession
with open(args.input) as file:
    gses_accs = list({gse.strip('\n') for gse in file.readlines() if gse})

# Get GEO objects using GEO parse
print("Consulting NCBI GEO...")
m = len(gses_accs)
gses = [gse_obj for i,gse in enumerate(gses_accs) if (gse_obj := get_GEO(gse, args.outfile, i, m, delete=True))]

# Get metadata from GEO objects
print("Parsing metadata...")
metadata = [gseMeta(gse).getAllMeta() for gse in gses]

# Print output
print("Building output...")
table = pd.concat(metadata)
table.to_csv(args.outfile, sep='\t', index=False)

if args.gpl: 
     gpls = {acc:gpl for gse in gses for acc, gpl in gse.gpls.items()}
     for acc, gpl in gpls.items():
          gpl.table.to_csv(os.path.join(os.path.split(args.outfile)[0], f"{acc}.txt"), sep='\t', index=False)

print("Done!")