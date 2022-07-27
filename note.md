# To create a list of duplicate SNPs
% less iSelect.vcf | awk '{print $2}'| uniq -c -d > duplicates.txt

# To get the chromosome ID instead that are duplicated. Re-map again to get chromosome ID instead of positions 
% while read line; do grep $line iSelect.vcf | awk '{print $3}' >> header.txt; done < duplicates.txt

# Do the same thing again this time and map the duplicate ID to the SAM file and cut out the information needed
% while read line; do grep $line iSelect_cowpea_BWA.sam | awk '{print $1,$3,$5,$6,$10}' >> result.txt; done < header.txt

# To make it a SAM file
% while read line; do grep $line iSelect_cowpea_BWA.sam >> result.txt; done < header.txt

# Use the script that I made for final comparing process