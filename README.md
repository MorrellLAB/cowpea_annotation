# Illumina cowpea iSelect SNP annotation

*   The ~51K SNPs on the iSelect Illumina genotyping platform [Muñoz-Amatriaín et al. 17](https://doi.org/10.1111/tpj.13404) have positional information relative to the cowpea reference genome IT97K-499-35 but not all positions are accurate. There is limited information on gene names, the class of variants, etc. We will use two primary annotation tools to identify SNP positions and gene names.

## Using SNP_utils to identify SNP positions

*   [SNP_Utils](https://github.com/MorrellLAB/SNP_Utils) implements multiple approaches for the identification of SNP positions. This is a fork of Paul Hoffman's original [SNP_Utils](https://github.com/mojaveazure/SNP_Utils)
*   The repository for updating the barley Morex reference also contains useful code [morex_reference](https://github.com/MorrellLAB/morex_reference).

## Using SNPMeta to identify genes names

*   [SNPMeta](https://github.com/MorrellLAB/SNPMeta) is a BLAST parser that identifies the genes in which SNPs occur and can identify the nature of mutations (e.g., synonymous versus nonsynonymous). SNPMeta design and usage is detailed in  [Kono et al. 2014](https://doi.org/10.1111/1755-0998.12183).
