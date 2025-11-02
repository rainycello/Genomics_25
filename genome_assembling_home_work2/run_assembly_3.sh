#!/bin/bash
# ==========================================================
#  SPAdes + QUAST automated benchmarking script
#  with Conda environment switching
# ==========================================================

# Define parameters
kmers=(21 33 55 77)
reads1="illumina1.fq"
reads2="illumina2.fq"
ref="seq.fa"
output_file="kmer_assembly_stats.txt"

# ------------------------- Header -------------------------
echo -e "kmer\tRuntime_sec\tNum_contigs\tTotal_length\tN50\tL50" > "$output_file"

# ------------------------- Main Loop -------------------------
for k in "${kmers[@]}"; do
  echo "=============================================="
  echo "🔹 Starting assembly for k=$k"
  echo "=============================================="
  outdir="spades_k${k}"
  start=$(date +%s)

  # ----------------------------------------------------------
  # 1️⃣ Activate environment for SPAdes
  # ----------------------------------------------------------
  echo "🧬 Activating Conda environment: genomika (for SPAdes)"
  source ~/anaconda3/etc/profile.d/conda.sh
  conda activate genomika

  # Run SPAdes
  echo "🚀 Running SPAdes..."
  spades.py -1 "$reads1" -2 "$reads2" -k "$k" -o "$outdir" --only-assembler > "$outdir.log" 2>&1
  end=$(date +%s)
  runtime=$((end - start))

  # ----------------------------------------------------------
  # Check if SPAdes produced contigs
  # ----------------------------------------------------------
  contigs_file="$outdir/contigs.fasta"
  if [[ ! -f "$contigs_file" ]]; then
      echo "⚠️  No contigs.fasta found for k=$k. Skipping..."
      echo -e "${k}\t${runtime}\tNA\tNA\tNA\tNA" >> "$output_file"
      continue
  fi

  # ----------------------------------------------------------
  # 2️⃣ Activate environment for QUAST
  # ----------------------------------------------------------
  echo "📊 Activating Conda environment: dmyboi (for QUAST)"
  conda deactivate
  conda activate dmyboi

  echo "📈 Running QUAST analysis..."
  quast -R "$ref" -o "$outdir/quast_report" "$contigs_file" > "$outdir/quast.log" 2>&1
  report="$outdir/quast_report/report.txt"

  # ----------------------------------------------------------
  # Validate QUAST report and extract metrics
  # ----------------------------------------------------------
  if [[ ! -f "$report" ]]; then
      echo "⚠️  No QUAST report for k=$k. Skipping..."
      echo -e "${k}\t${runtime}\tNA\tNA\tNA\tNA" >> "$output_file"
      continue
  fi

  num_contigs=$(grep -m1 "# contigs" "$report" | awk '{print $NF}')
  total_length=$(grep -m1 "Total length" "$report" | awk '{print $NF}')
  n50=$(grep -m1 "^N50" "$report" | awk '{print $NF}')
  l50=$(grep -m1 "^L50" "$report" | awk '{print $NF}')

  num_contigs=${num_contigs:-NA}
  total_length=${total_length:-NA}
  n50=${n50:-NA}
  l50=${l50:-NA}

  echo "✅ k=$k finished."
  echo "   Runtime: ${runtime}s | Contigs: $num_contigs | N50: $n50 | L50: $l50"
  echo -e "${k}\t${runtime}\t${num_contigs}\t${total_length}\t${n50}\t${l50}" >> "$output_file"

  # ----------------------------------------------------------
  # 3️⃣ Cleanup (optional)
  # ----------------------------------------------------------
  # Uncomment this to clean after each run:
  # rm -rf "$outdir"

  # Return to base environment to prepare for next run
  conda deactivate
done

# ------------------------- Summary -------------------------
echo
echo "🎉 Finished all assemblies!"
echo "📁 Results saved to: $output_file"
echo "You can preview results with: cat $output_file"
