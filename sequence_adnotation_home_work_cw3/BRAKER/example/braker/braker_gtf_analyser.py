#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

gtf = "braker.gtf"

genes = defaultdict(lambda: {"transcripts": set(), "exons": []})

# --- Parse GTF ---
with open(gtf) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        fields = line.strip().split("\t")
        if len(fields) < 9:
            continue
        feature = fields[2]
        start, end = int(fields[3]), int(fields[4])
        attrs = fields[8]

        # Parse attributes
        attrs_dict = {}
        for a in attrs.split(";"):
            a = a.strip()
            if not a:
                continue
            if " " in a:
                key, val = a.split(" ", 1)
                attrs_dict[key] = val.strip('"')
        gene_id = attrs_dict.get("gene_id", None)
        transcript_id = attrs_dict.get("transcript_id", None)

        if not gene_id:
            continue

        if transcript_id:
            genes[gene_id]["transcripts"].add(transcript_id)

        if feature == "exon":
            genes[gene_id]["exons"].append((start, end))

# --- Compute stats ---
gene_lengths = []
exon_lengths = []
intron_lengths = []
exons_per_gene = []
transcripts_per_gene = []

for gene_id, data in genes.items():
    if not data["exons"]:
        continue
    exons = sorted(data["exons"])
    gene_start, gene_end = exons[0][0], exons[-1][1]
    gene_len = gene_end - gene_start + 1
    gene_lengths.append(gene_len)

    # exon stats
    exon_lens = [end - start + 1 for start, end in exons]
    exon_lengths.extend(exon_lens)
    exons_per_gene.append(len(exon_lens))

    # intron stats
    for i in range(1, len(exons)):
        intron_len = exons[i][0] - exons[i - 1][1] - 1
        if intron_len > 0:
            intron_lengths.append(intron_len)

    # transcript stats
    transcripts_per_gene.append(len(data["transcripts"]))

# --- Compute summary metrics ---
summary = {
    "Liczba genów": len(genes),
    "Śr. długość genu (bp)": sum(gene_lengths) / len(gene_lengths),
    "Śr. długość eksonu (bp)": sum(exon_lengths) / len(exon_lengths),
    "Śr. długość intronu (bp)": sum(intron_lengths) / len(intron_lengths),
    "Śr. liczba egzonów/gen": sum(exons_per_gene) / len(exons_per_gene),
    "Śr. liczba transkryptów/gen": sum(transcripts_per_gene) / len(transcripts_per_gene)
}

# --- Print summary ---
print("\n===== STATYSTYKI ADNOTACJI (BRAKER) =====")
for k, v in summary.items():
    print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")
print("==========================================\n")

# --- Plot ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].hist(gene_lengths, bins=50)
axes[0, 0].set_title("Długości genów (bp)")
axes[0, 0].set_xlabel("Długość [bp]"); axes[0, 0].set_ylabel("Liczba genów")

axes[0, 1].hist(exon_lengths, bins=50)
axes[0, 1].set_title("Długości eksonów (bp)")
axes[0, 1].set_xlabel("Długość [bp]"); axes[0, 1].set_ylabel("Liczba eksonów")

axes[1, 0].hist(intron_lengths, bins=50)
axes[1, 0].set_title("Długości intronów (bp)")
axes[1, 0].set_xlabel("Długość [bp]"); axes[1, 0].set_ylabel("Liczba intronów")

axes[1, 1].boxplot([exons_per_gene, transcripts_per_gene],
                   labels=["Egzony/gen", "Transkrypty/gen"])
axes[1, 1].set_title("Struktura genów")
axes[1, 1].set_ylabel("Liczba")

plt.suptitle("Analiza adnotacji BRAKER (braker.gtf)", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
