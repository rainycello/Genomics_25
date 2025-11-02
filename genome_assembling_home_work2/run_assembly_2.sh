#!/bin/bash

kmers=(21 33 55 77)
reads1="illumina1.fq"
reads2="illumina2.fq"
ref="seq.fa"
output_file="kmer_assembly_stats.txt"

echo -e "kmer\tRuntime_sec\tNum_contigs\tTotal_length\tN50\tL50" > $output_file

for k in "${kmers[@]}"
do
  echo "Starting assembly for k=$k"
  outdir="spades_k${k}"

  start=$(date +%s)
  spades.py -1 $reads1 -2 $reads2 -k $k -o $outdir --only-assembler
  end=$(date +%s)
  runtime=$((end - start))

  quast -R $ref -o $outdir/quast_report $outdir/contigs.fasta
  
  report=$outdir/quast_report/report.txt

  num_contigs=$(awk '/^# contigs/ {print $NF; exit}' $report)
  total_length=$(awk '/^Total length/ {print $NF; exit}' $report)
  n50=$(awk '/^N50/ {print $NF; exit}' $report)
  l50=$(awk '/^L50/ {print $NF; exit}' $report)

  echo -e "${k}\t${runtime}\t${num_contigs}\t${total_length}\t${n50}\t${l50}" >> $output_file

  rm -rf $outdir
done

echo "Finished! Results saved in $output_file"

