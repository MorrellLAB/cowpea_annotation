#!/bin/bash -l
#SBATCH --time=4:00:00
#SBATCH --ntasks=8
#SBATCH --mem=10g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=pmorrell@umn.edu

# This scirpt is designed to require three arguments.
# 1) full path to SAM aligment, 2) full path to uncompressed reference genome, 3) full path to output directory
[ $# -eq 0 ] && { echo "Usage: $0 'full path to .sam file' and 'full path to reference genome'"; exit 1; }

module load python3/3.6.3_anaconda5.0.1

#  Set path to SNP_Utils directory
SNP_Utils_dir=/panfs/roc/groups/9/morrellp/shared/Software/SNP_Utils
SNP_Utils="${SNP_Utils_dir}/snp_utils.py"
SNPs=/panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/iSelect_all.txt
SAM=$1
REF=$2
MAP=/panfs/roc/groups/9/morrellp/pmorrell/Workshop/Cowpea/SNP_Utils/Cowpea_consesus_map_plink_2.txt
OUT_DIR=$3
DIR=$(basename "$SAM" .sam)

cd "${SNP_Utils_dir}" || exit
python3 "${SNP_Utils}" SAM \
--lookup "${SNPs}" \
--sam-file "${SAM}" \
--reference "${REF}" \
--by-chrom --genetic-map "${MAP}" \
--outname "${OUT_DIR}/${DIR}"
