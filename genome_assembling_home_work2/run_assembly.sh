#!/bin/bash

kmers=(21 33 55 77)
reads1="illumina1.fq"
reads2="illumina2.fq"
ref="seq.fa"
output_file="kmer_assembly_stats.txt"

echo -e "kmer\tRuntime_sec\tNum_contigs\tTotal_length\tN50\tL50" > $output_file

for k in "${kmers[@]}"
do
  echo "Running assembly for k=$k"
  outdir="spades_k${k}"

  # Measure runtime
  start=$(date +%s)
  spades.py -1 $reads1 -2 $reads2 -k $k -o $outdir --only-assembler
  end=$(date +%s)
  runtime=$((end - start))

  # Run QUAST
  quast -R $ref -o $outdir/quast_report $outdir/contigs.fasta

  # Extract stats from QUAST's report.txt
  num_contigs=$(grep "^# contigs" $outdir/quast_report/report.txt | head -1 | awk '{print $4}')
  total_length=$(grep "^Total length" $outdir/quast_report/report.txt | head -1 | awk '{print $4}')
  n50=$(grep "^N50" $outdir/quast_report/report.txt | head -1 | awk '{print $2}')
  l50=$(grep "^L50" $outdir/quast_report/report.txt | head -1 | awk '{print $2}')

  # Append to output file
  echo -e "${k}\t${runtime}\t${num_contigs}\t${total_length}\t${n50}\t${l50}" >> $output_file

  # Clean up
  rm -rf $outdir
done

echo "Statistics saved to $output_file"
