from Bio import Entrez
import xml.etree.ElementTree as ET

# Set your email (and API key if available)
Entrez.email = "trejantwesige19@gmail.com"

def fetch_gene_info(gene_symbol, organism="Homo sapiens"):
    """Fetch gene details from NCBI for a given gene symbol and organism."""
    query = f"{gene_symbol}[Gene] AND {organism}[Organism]"
    print(f"Query: {query}")
    
    try:
        # Search for the gene in the NCBI Gene database
        search_handle = Entrez.esearch(db="gene", term=query)
        search_record = Entrez.read(search_handle)
        search_handle.close()
        
        if search_record["IdList"]:
            gene_id = search_record["IdList"][0]
            print(f"Found {gene_symbol} with Gene ID: {gene_id}")
            
            # Fetch detailed gene information using the Gene ID
            fetch_handle = Entrez.efetch(db="gene", id=gene_id, retmode="xml")
            data = fetch_handle.read()
            fetch_handle.close()
            
            # Parse XML to extract details
            root = ET.fromstring(data)
            for gene in root.findall(".//Entrezgene"):
                gene_info = {
                    "GeneID": gene.findtext(".//Gene-track_geneid"),
                    "Symbol": gene.findtext(".//Gene-ref_locus"),
                    "Description": gene.findtext(".//Gene-ref_desc")
                }
                print("\nGene Information:")
                for key, value in gene_info.items():
                    print(f"  {key}: {value}")
            
            return data
        else:
            print(f"No results found for {gene_symbol} in {organism}.")
            return None

    except Exception as e:
        print(f"Error fetching {gene_symbol}: {e}")
        return None


# List of obesity-related genes to fetch
genes = ["FTO", "MC4R", "LEP", "LEPR", "APOA2", "PPARG", "ADIPOQ", "UCP1"]

if __name__ == "__main__":
    for gene in genes:
        print(f"\nFetching data for {gene}...")
        fetch_gene_info(gene)
