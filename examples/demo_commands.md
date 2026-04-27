# Demo commands

# Find BRD4 TF ChIP-seq FASTQs, write sheets (no downloads)
encodefetch --assay-title "TF ChIP-seq" --target-label BRD4 --file-type fastq --status released --nfcore --snakemake

# Accessions mode
encodefetch --accessions ENCSR514EOE,ENCSR395MHA --file-type fastq --progress

# Accessions file mode
encodefetch --accessions accessions.txt --file-type fastq --nfcore

# Human unperturbed, multiple targets
encodefetch --assay-title "TF ChIP-seq" --target-label BRD4 --target-label SMAD3 --organism "Homo sapiens" --perturbed false --file-type fastq
