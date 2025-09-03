# Demo commands

# Find BRD4 TF ChIP-seq FASTQs, write sheets (no downloads)
encode-fetch --assay-title "TF ChIP-seq" --target-label BRD4 --file-type fastq --status released --nfcore --snakemake

# Accessions mode
encode-fetch --accessions ENCSR514EOE,ENCSR395MHA --file-type fastq --progress

# Human unperturbed, multiple targets
encode-fetch --assay-title "TF ChIP-seq" --target-label BRD4 --target-label SMAD3 --organism "Homo sapiens" --perturbed false --file-type fastq
