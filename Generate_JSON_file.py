import json
import sys

def parse_fasta(file_path):
    fasta_sequences = []
    with open(file_path, 'r') as f:
        header = ''
        sequence = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    fasta_sequences.append((header, sequence))
                header = line[1:]
                sequence = ''
            else:
                sequence += line
        if header and sequence:
            fasta_sequences.append((header, sequence))
    return fasta_sequences

def main(dna_fasta_file, protein_fasta_file, output_file):
    
    dna_sequences = parse_fasta(dna_fasta_file)
    
    
    protein_sequence = None
    with open(protein_fasta_file, 'r') as f:
        protein_sequence = f.read().strip()

   
    json_objects = []

    
    for i, (dna_header, dna_sequence) in enumerate(dna_sequences):
       
        json_obj = {
            "name": f"Job_{i+1}_{dna_header}",
            "modelSeeds": [],
            "sequences": [
                {
                    "proteinChain": {
                        "sequence": protein_sequence,
                        "count": 1
                    }
                },
                {
                    "dnaSequence": {
                        "sequence": dna_sequence,
                        "count": 1
                    }
                }
            ]
        }
        
    
        json_objects.append(json_obj)

    
    with open(output_file, 'w') as f:
        json.dump(json_objects, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py dna_fasta_file protein_fasta_file output_file")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
