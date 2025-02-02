from Bio import Entrez
import xml.etree.ElementTree as ET

# Set your email (and leave API key empty if not using one)
Entrez.email = "trejantwesige19@gmail.com"
# Entrez.api_key = ""  # Not using an API key for now

def fetch_gene_info(gene_symbol):
    # Use a minimal query with just the gene symbol
    query = gene_symbol
    print("Query:", query)
    
    try:
        # Search for the gene in the NCBI Gene database; retmax=1 limits to the top result
        search_handle = Entrez.esearch(db="gene", term=query, retmax=1)
        search_record = Entrez.read(search_handle)
        search_handle.close()
    except Exception as e:
        print("Error during esearch:", e)
        return None
    
    if search_record["IdList"]:
        gene_id = search_record["IdList"][0]
        print(f"Found {gene_symbol} with Gene ID: {gene_id}")
        
        try:
            # Fetch detailed gene information using the Gene ID
            fetch_handle = Entrez.efetch(db="gene", id=gene_id, retmode="xml")
            data = fetch_handle.read()
            fetch_handle.close()
        except Exception as e:
            print("Error during efetch:", e)
            return None
        
        # Parse the XML data to extract key details
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
        print(f"No results found for {gene_symbol}.")
        return None

# Example usage: Fetch details for the FTO gene
if __name__ == "__main__":
    gene_data = fetch_gene_info("FTO")
