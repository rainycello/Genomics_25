#!/bin/bash
# ==========================================================
#  SPAdes + QUAST automated benchmarking script
#  with dynamic Conda activation
# ==========================================================

kmers=(21 33 55 77)
reads1="illumina1.fq"
reads2="illumina2.fq"
ref="seq.fa"
output_file="kmer_assembly_stats.txt"

echo -e "kmer\tRuntime_sec\tNum_contigs\tTotal_length\tN50\tL50" > "$output_file"

# Pobierz ścieżkę do Condy
conda_base=$(conda info --base)
source "$conda_base/etc/profile.d/conda.sh"

for k in "${kmers[@]}"; do
  echo "=============================================="
  echo "🔹 Starting assembly for k=$k"
  echo "=============================================="
  outdir="spades_k${k}"

  start=$(date +%s)

  # ----------------------------------------------------------
  # 1️⃣ SPAdes — genomika
  # ----------------------------------------------------------
  echo "🧬 Activating Conda environment: genomika (SPAdes)"
  conda activate genomika
  spades.py -1 "$reads1" -2 "$reads2" -k "$k" -o "$outdir" --only-assembler > "$outdir.log" 2>&1
  end=$(date +%s)
  runtime=$((end - start))

  contigs_file="$outdir/contigs.fasta"
  if [[ ! -f "$contigs_file" ]]; then
      echo "⚠️ No contigs.fasta found for k=$k"
      echo -e "${k}\t${runtime}\tNA\tNA\tNA\tNA" >> "$output_file"
      continue
  fi

  # ----------------------------------------------------------
  # 2️⃣ QUAST — dmyboi
  # ----------------------------------------------------------
  echo "📊 Activating Conda environment: dmyboi (QUAST)"
  conda deactivate
  conda activate dmyboi

  quast -R "$ref" -o "$outdir/quast_report" "$contigs_file" > "$outdir/quast.log" 2>&1
  report="$outdir/quast_report/report.txt"

  if [[ ! -f "$report" ]]; then
      echo "⚠️ No QUAST report for k=$k"
      echo -e "${k}\t${runtime}\tNA\tNA\tNA\tNA" >> "$output_file"
      continue
  fi

  # ✅ Lepsze wyciąganie wartości z raportu
  num_contigs=$(grep -m1 -E "^# contigs" "$report" | awk '{print $(NF)}')
  total_length=$(grep -m1 -E "^Total length" "$report" | awk '{print $(NF)}')
  n50=$(grep -m1 -E "^N50" "$report" | awk '{print $(NF)}')
  l50=$(grep -m1 -E "^L50" "$report" | awk '{print $(NF)}')

  num_contigs=${num_contigs:-NA}
  total_length=${total_length:-NA}
  n50=${n50:-NA}
  l50=${l50:-NA}

  echo "✅ k=$k finished."
  echo "   Runtime: ${runtime}s | Contigs: $num_contigs | N50: $n50 | L50: $l50"
  echo -e "${k}\t${runtime}\t${num_contigs}\t${total_length}\t${n50}\t${l50}" >> "$output_file"

  # Wróć do bazowego środowiska
  conda deactivate
done

echo
echo "🎉 Finished all assemblies!"
echo "📁 Results saved to: $output_file"
