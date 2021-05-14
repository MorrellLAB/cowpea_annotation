# Cowpea annotation workflow


## The reference genome for Vicia unguiculata, IT97K-499-35


```bash
cd /scratch.global/pmorrell/Cowpeapan/VunguiculataIT97K-499-35_v1.2/assembly
md5sum Vunguiculata_IT97K-499-35_v1.0.fa.gz
[//]: # 78686a7ec556ad59fc2612432ae8fef3  Vunguiculata_IT97K-499-35_v1.0.fa.gz
[//]: # Unfortunately the checksums don't match! Try pulling directly from Phytozome and checking again!
[//]: # Try another genome: VunguiculataSuvita2_541_v1.1
*    Md5 checksum listed as: `b9a318fa49d247f79f1d48538f18d205`

cd /scratch.global/pmorrell/Cowpeapan/VunguiculataSuvita2_541_v1.1/assembly
md5sum VunguiculataSuvita2_541_v1.0.fa.gz
[//]: # 24903399b8a6f2311a9e5b7300079daf  VunguiculataSuvita2_541_v1.0.fa.gz
```
*   To format a blast database from the reference genome we need to use a command line similar to that from this [link](https://github.com/lilei1/9k_BOPA_SNP/tree/617faed6534ddbf94c287636a068ac4c4f5b25c8/BOPA_9k_vcf_Morex_refv1). The command looks like: ```makeblastdb -in 160404_barley_pseudomolecules_masked.fasta -dbtype nucl -parse_seqids```. The


##Setting up contextual sequence for annotation

*   Using iSelect contextual sequence as provided in a file from Tim Close, "iSelect_DesignSequences.xlxs"
*   SNPs have 60 bp of sequence on the 5' side, but sometimes contextual sequence is shorter on the 3'

```bash
[//]: # File in Dropbox
cd /Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea
[//]: # Remove the header line and preserve only the name and the
 tail -n +2 /Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea/iSelect_DesignSequences.txt | awk 'BEGIN {FS="\t"}; {print $1, $8}' >iSelect_all.txt
wc -l iSelect_all.txt
[//]: #    56719 iSelect_all.txt - there are many additional variants that did not make the assay.
[//]: #  Planning to annotate everything, including those that are indicated on the spreadsheet as not being on the iSelect chip!
```

*   Moved the file over to MSI for analysis
*   Converting the tab-delimited SNPs to a fasta file.

```bash
cd /panfs/roc/groups/9/morrellp/shared/Datasets/Annotations/Cowpea
[//]: #  Make sure we are using tab delimited text
perl -p -i -e 's/ /\t/g' iSelect_all.txt
module load python2
[//]: #  Have to use Python 2 for the helper scripts
python2 --version
[//]: #  Python 2.7.15 :: Anaconda, Inc.
python2 ~/shared/Software/SNPMeta/Helper_Scripts/Convert_Illumina.py iSelect_all.txt >iSelect_all.fas

srun -N 1 --ntasks-per-node=4  --mem-per-cpu=1gb -t 1:00:00 -p interactive --pty bash

module load python3/3.8.3_anaconda2020.07_mamba
module load ncbi_blast+/2.8.1
module load emboss/6.6.0

[//]: #  Have to use a very specific version of Biopython!
pip install biopython==1.69 --user

[//]: # Used head to pull just the beginning of the fasta file.
python3 ~/shared/Software/SNPMeta/SNPMeta.py -f cowpea_100.fas \
-a 'pmorrell@umn.edu' \
-l 60 \
--outfmt tabular \
-o 'cowpea_SNPMeta.txt'
```

## Cowpea SNP annotation

Peter L. Morrell\
28 April 2021

*   Check our input file, it looks like there are Windows line endings (from the spreadsheet export)
*   Fix those below

```bash
file /Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea/iSelect_all.txt
/Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea/iSelect_all.txt: ASCII text, with CRLF line terminators

sed -i.bak 's/\r$//'  /Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea/iSelect_all.txt
pmorrell@x-134-84-0-93 Utilities % file /Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea/iSelect_all.txt
/Users/pmorrell/Dropbox/Documents/Work/Projects/Cowpea/iSelect_all.txt: ASCII text
```

*   Using the setup from Li Lei's run of [9k_BOPA_SNP](https://github.com/lilei1/9k_BOPA_SNP/tree/617faed6534ddbf94c287636a068ac4c4f5b25c8/BOPA_9k_vcf_Morex_refv1)
*   Used example from Li Lei to write a new Slurm bash script for BLAST makeblashdb. Was so fast it did not need to queue.
*   The [makeblastdb.sh](https://github.com/pmorrell/Utilities/blob/master/makeblastdb.sh) script is at the link
*   First run the [SNP_Utils](https://github.com/MorrellLAB/SNP_Utils) CONFIG step to make a config file for BLAST search
*   Use [SNPMeta]https://github.com/MorrellLAB/SNPMeta helper script to convert iSelect contextual sequence for read mapping in BWA MEM
  *    [Convert_Illumina.py](https://github.com/MorrellLAB/SNPMeta/blob/master/Helper_Scripts/Convert_Illumina.py)
  *    Need to create a bwa index

```bash
module load python3
pip install overload --user

cd /panfs/roc/groups/9/morrellp/shared/Software/SNP_Utils
 ./snp_utils.py  CONFIG -d /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.fa -k -i 95 -c /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.ini

./snp_utils.py BLAST -l /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/iSelect_all.txt \
-c /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.ini \
 -b -d -t 100000 -o /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.vcf
```



## Identifying cowpea SNP positions using SNP_Utils

Peter Morrell and Nadia Janis\
4 May 2021\
Falcon Heights, MN

### Data Preparation
*   Need to load NCBI BLAST
```bash
cd /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils
module load ncbi_blast+/2.8.1
wget https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz
tar zxvf taxdb.tar.gz

makeblastdb -in Vunguiculata_IT97K-499-35_v1.0.fa -dbtype nucl -parse_seqids

blastdbcheck -db Vunguiculata_IT97K-499-35_v1.0.fa
blastn -db Vunguiculata_IT97K-499-35_v1.0.fa \
-query iSelect_all.fas \
-outfmt 5
-out cowpea_snps.xml &
[//]: # outfmt 5 is xml
```
*   Preparing genetic map for [SNP_Utils](https://github.com/MorrellLAB/SNP_Utils?organization=MorrellLAB&organization=MorrellLAB)
*   Need to replace linkage group names with names on chromosomes
*   The genetic map needs to be in Plink 1.9 format. This requires a 1-based physical position in the fourth column.


```bash
perl -wpl -e 's/\b1\t/Vu01/g;' | \
perl -wpl -e 's/\b2\t/Vu02/g;' | \
perl -wpl -e 's/\b3\t/Vu03/g;' | \
perl -wpl -e 's/\b4\t/Vu04/g;' | \
perl -wpl -e 's/\b5\t/Vu05/g;' | \
perl -wpl -e 's/\b6\t/Vu06/g;' | \
perl -wpl -e 's/\b7\t/Vu07/g;' | \
perl -wpl -e 's/\b8\t/Vu08/g;' | \
perl -wpl -e 's/\b9\t/Vu09/g;' | \
perl -wpl -e 's/\b10\t/Vu10/g;' | \
perl -wpl -e 's/\b11\t/Vu11/g;' >cowpea_consensus_map.txt
```
```bash
cd Desktop
wc -l Cowpea_consensus_map.txt
[//]: # 37,371 SNPs are in the consensus map, need to add 1 value, as the numbers are 1-based.
paste Cowpea_consensus_map.txt <(seq 1 37372) >~/Desktop/Cowpea_consesus_map_plink.txt

```



```bash
module load python3/3.6.3_anaconda5.0.1
cd /panfs/roc/groups/9/morrellp/shared/Software/SNP_Utils
GENETIC_MAP=/panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Cowpea_consensus_map_plink.txt
LOOKUP_TABLE=/panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/iSelect_all.txt
REFERENCE=/panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.fa
XML=/panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/cowpea_snps.xml
OUT_PREFIX=cowpea_iSelect
python3 snp_utils.py BLAST -l ${LOOKUP_TABLE} -x ${XML} -b -m ${GENETIC_MAP} -d -t 100000 -o ${OUT_PREFIX}
```

## Getting to final results!

Peter Morrell\
05 May 2021\
Falcon Heights, MN

```bash
module load python3/3.6.3_anaconda5.0.1
cd /panfs/roc/groups/9/morrellp/shared/Software/SNP_Utils
python3 snp_utils.py SAM \
--lookup /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/iSelect_all.txt \
--sam-file /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea_BWA.sam \
--reference /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Vunguiculata_IT97K-499-35_v1.0.fa \
--by-chrom --genetic-map /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Cowpea_consesus_map_plink.txt \
--outname /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea
```

>Reading in lookup table /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/iSelect_all.txt
>Reading in reference FASTA /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/>Vunguiculata_IT97K-499-35_v1.0.fa This might take a while...
>Reading in SAM file /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea_BWA.sam
>No map for 1_0661
>No map for 2_02646
>No map for 2_48680
>No map for 2_51194
>Filtering SNPs by hit chromsome/contig
>Using genetic map /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Cowpea_consesus_map_plink.txt
>Writing 56701 SNPs to /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea.vcf
>Removing masked SNPs that were actually found
>Writing 14 masked SNPs to /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/>iSelect_cowpea_masked.vcf
>Writing 4 failed SNPs to /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa/iSelect_cowpea_failed.log

*   Creating files for Tim Close

```bash
cd /panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/bwa

grep -v '#' iSelect_cowpea.vcf | awk 'BEGIN {FS="\t"}; {print $3,$1,$2}' >SNP_positions.txt
join Tim_table.txt <(sort -k1 SNP_positions.txt) | cut -d ' ' -f 1,4,5,6 >Tim_new.txt
```


## Another try with the BLAST version of SNP\_Utils after cleaning input



Peter Morrell\
06 May 2021\
Falcon Heights, MN

*   Reran the [blastn.sh]() script with the "-" characters removed from SNP contextual sequences
*
