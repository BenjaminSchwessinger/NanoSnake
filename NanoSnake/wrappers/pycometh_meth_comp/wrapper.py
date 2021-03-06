__author__ = "Adrien Leger"
__copyright__ = "Copyright 2019, Adrien Leger"
__email__ = "aleg@ebi.ac.uk"
__license__ = "MIT"
__version__ = "0.0.1"

# Imports
import os
from snakemake.shell import shell

# Shortcuts
opt = snakemake.params.get("opt", "")
input_tsv = snakemake.input.tsv
ref = snakemake.input.ref
output_tsv = snakemake.output.get("tsv", "")
output_bed = snakemake.output.get("bed", "")
output_bed_index = snakemake.output.get("bed_index", "")

# Get sample_id_list
sample_id_list = snakemake.params.get("sample_id_list", None)
if not sample_id_list:
    try:
        sample_id_list = []
        for fn in input_tsv:
            if fn.endswith(".gz"):
                sample_id_list.append(os.path.basename(fn).rpartition(".")[0].rpartition(".")[0])
            else:
                sample_id_list.append(os.path.basename(fn).rpartition(".")[0])
    except Exception:
        sample_id_list = [f"S{i}" for i in range(1, len(input_tsv)+1)]

# Convert list to str
if isinstance(sample_id_list, list):
    sample_id_list = " ".join(sample_id_list)

# Define conditional IO
output = ""
if output_tsv:
    output += f" -t {output_tsv} "
if output_bed:
    output += f" -b {output_bed} "

# Run shell command
shell(f"pycoMeth Meth_Comp {opt} -i {input_tsv} -f {ref} {output} -s {sample_id_list} 2> {snakemake.log}")

# Optional Indexing with igv
if output_bed_index and output_bed_index.endswith(".idx") and output_bed and output_bed.endswith(".bed"):
    shell(f"igvtools index {output_bed} &>> {snakemake.log}")
