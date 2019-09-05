__author__ = "Adrien Leger"
__copyright__ = "Copyright 2019, Adrien Leger"
__email__ = "aleg@ebi.ac.uk"
__license__ = "MIT"

# Imports
import os
from snakemake.shell import shell

# Get optional args if unavailable
opt = snakemake.params.get("opt", "")

# Run shell commands
shell("nanopolish call-methylation -t {snakemake.threads} {opt} -r {snakemake.input.fastq} -b {snakemake.input.bam} -g {snakemake.input.ref} > {snakemake.output} 2> {snakemake.log}")
