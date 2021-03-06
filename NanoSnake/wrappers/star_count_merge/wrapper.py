__author__ = "Adrien Leger"
__copyright__ = "Copyright 2019, Adrien Leger"
__email__ = "aleg@ebi.ac.uk"
__license__ = "MIT"
__version__ = "0.0.1"

# Imports
from snakemake.shell import shell
import pandas as pd
import os

# Shortcuts
input_counts = snakemake.input.counts
unstranded_counts = snakemake.output.get("unstranded_counts", None)
positive_counts = snakemake.output.get("positive_counts", None)
negative_counts = snakemake.output.get("negative_counts", None)

for col_num, output_counts in ((1,unstranded_counts),(2,positive_counts),(3,negative_counts)):
    if output_counts:
        df = pd.DataFrame()
        for c in input_counts:
            sample_id = os.path.basename(c).rpartition(".")[0]
            sample_df = pd.read_csv(c, sep="\t", names=["gene_id", sample_id], index_col=0, usecols=[0,col_num])
            sample_df = sample_df.dropna()
            df = df.join(sample_df, how='outer')
        df = df.fillna(0)
        df.to_csv(output_counts, sep="\t")
