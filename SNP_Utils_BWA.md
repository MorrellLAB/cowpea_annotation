# Identifying SNP locations

*   To identify SNP locations, we are using contextual sequence for individual variants mapped to a reference genome using standard short sequence read mapping software. I've used [BWA MEM](https://github.com/lh3/bwa) but [bowtie](https://github.com/BenLangmead/bowtie) should also work to create a [SAM](https://samtools.github.io/hts-specs/SAMv1.pdf) alignment file.
*   We process the SAM file with a custom Python program [SNP_Utils](https://github.com/MorrellLAB/SNP_Utils?organization=MorrellLAB&organization=MorrellLAB). The SNP_Utils [Github](https://github.com/MorrellLAB/SNP_Utils?organization=MorrellLAB&organization=MorrellLAB) page includes extensive documentation, including a list of dependencies.
*   SAM alignments can be viewed and sorted using [samtools](http://www.htslib.org/doc/samtools.html). Mapping quality scores are the most useful information, and are in the fifth column of the SAM file.


## Preparation to run SNP_Utils

*   1) Create an index of the reference genome to be used with BWA. This uses the `bwa index` command, and should run quickly.
*   2) Identify the contextual sequence for the SNPs you wish to map. You need both a tab-delimited [file](https://www.dropbox.com/s/16uqe9o3eogrygd/iSelect_all.txt?dl=0) with SNP names and contextual sequence in "Illumina-format" and a fasta [file](https://www.dropbox.com/s/2slw1gnyjkxevb0/iSelect_all.fas?dl=0) with the same information. Some tools in the workflow are intolerant of extraneous characters, particularly in the fasta file. Consider using `grep -i -E '[^ACTGNKMRSWY]+' iSelect_all.fas` (with your file name) to identify extraneous characters. There is a script to convert Illumina format to fasta [here](https://github.com/MorrellLAB/SNPMeta/blob/master/Helper_Scripts/Convert_Illumina.py). This script requires Python 2. At UMN MSI it is available as `module load python2/2.7.12_anaconda4.2`
*   3) Run `bwa mem` to map SNPs to the reference genome. There is an example script [here](https://github.com/pmorrell/Utilities/blob/master/bwa_mem.sh). At UMN MSI, bwa is available as `module load bwa/0.7.17`. This step runs quickly, but you can also us this [script](https://github.com/pmorrell/Utilities/blob/master/bwa_mem.sh) by modifying file paths.
*   4) Check your SAM alignment with samtools. Run `samtools flagstat iSelect_all.sam` (with your file name) to get read mapping statistics. The number of mapped reads should be very high, (i.e., ~99%). At UMN MSI, samtools is available as `module load samtools/1.9`.
*   5) Check your alignment using `samtools view iSelect_all.sam`. The fifth and sixth columns should have values similar to "60" for good mapping quality and "121M" for a clean match to the reference genome. If the last field contains values that start with "XA:", the SNP did not map uniquely. The string that follows "XA:" lists "alternative hits" or additional mapping locations. The string that starts with "SA:" includes supplementary alignments. The difference in these two types of alignments is a little unclear, but "SA:" may not map continously to one location.

## Run SNP_Utils

*   To use all of the functionality in SNP_Utils, you can also provide a genetic map in (plink 1.9)[https://www.cog-genomics.org/plink2/]. The format looks like the table below or this [file](https://www.dropbox.com/s/ns6l2oz2x5l0np4/Cowpea_consesus_map_plink_2.txt?dl=0). Of course you don't know the base-pair coordinates before running the analysis. Consider using `seq 1 10` where 10 is the number of SNPs + 1 and use the UNIX/Linux command line tool `join` to integrate this with the genetic map. SNP names should match those in other files. Fields should be tab-separated.

| Chromsome code | Variant identifier  | Position in morgans or centimorgans | Base-pair coordinate |
|:--|:--|:--|:--|
| Vu01 | 2_19235 | 0.00 | 1 |
| Vu01 | 2_28392  | 0.00 | 2 |
| Vu01 | 1_0052 | 0.19 | 6 |

*   Running SNP_Utils will look something like the code block below. Be sure to check SNP_Utils [Github](https://github.com/MorrellLAB/SNP_Utils?organization=MorrellLAB&organization=MorrellLAB) for dependencies and more example code. You can also use the bash script [SNP_Utils_cowpea.sh](https://github.com/MorrellLAB/cowpea_annotation/blob/main/SNP_Utils_cowpea.sh) by providing two arguments at runtime. These include the full path the '.sam' alignment file as detailed above and the full path to the reference genome being used. Currently the reference genome should be uncompressed.
*   **Getting the right version of Python 3 so that [biopython](https://biopython.org) is installed and available is non-trivial.** Consider using `pip install biopython==1.69 --user`.
*   **[Overload](https://pypi.org/project/overload/) can also be tough to install.** Consider using `pip install overload --user`.

```bash
module load python3/3.6.3_anaconda5.0.1
cd /panfs/roc/groups/9/morrellp/shared/Software/SNP_Utils
python3 snp_utils.py SAM \
--lookup /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/iSelect_all.txt \
--sam-file /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea_BWA.sam \
--reference /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.fa \
--by-chrom --genetic-map /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Cowpea_consesus_map_plink_2.txt \
--outname /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea_2
```
