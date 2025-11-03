#!/usr/bin/env python3
import os
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Pliki wejściowe
FILES = {
    "gene": {
        "AUGUSTUS": "augustus_gene_lengths.tsv",
        "BRAKER": "braker_gene_lengths.tsv"
    },
    "exon": {
        "AUGUSTUS": "augustus_exon_lengths.tsv",
        "BRAKER": "braker_exon_lengths.tsv"
    },
    "intron": {
        "AUGUSTUS": "augustus_intron_lengths.tsv",
        "BRAKER": "braker_intron_lengths.tsv"
    }
}

EXON_PER_GENE = {
    "AUGUSTUS": "augustus_exons_per_gene.txt",
    "BRAKER": "braker_exons_per_gene.txt"
}

TRANS_PER_GENE = {
    "AUGUSTUS": "augustus_trans_counts_per_gene.txt",
    "BRAKER": "braker_trans_counts_per_gene.txt"
}

def read_lengths(file_path):
    """Wczytuje 4. kolumnę z TSV"""
    data = []
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        data.append(int(parts[3]))
                    except:
                        pass
    return data

def read_counts(file_path):
    """Wczytuje pierwszy element z plików uniq -c"""
    data = []
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    try:
                        data.append(int(parts[0]))
                    except:
                        pass
    return data

# 🔹 Wczytaj dane do DataFrame
frames = []
for feature, methods in FILES.items():
    for method, path in methods.items():
        values = read_lengths(path)
        for v in values:
            frames.append({"feature": feature, "method": method, "length": v})

df = pd.DataFrame(frames)

# 🔹 Dodaj dane per gene
df_counts = []
for method, path in EXON_PER_GENE.items():
    vals = read_counts(path)
    for v in vals:
        df_counts.append({"feature": "exons_per_gene", "method": method, "count": v})
for method, path in TRANS_PER_GENE.items():
    vals = read_counts(path)
    for v in vals:
        df_counts.append({"feature": "transcripts_per_gene", "method": method, "count": v})
dfc = pd.DataFrame(df_counts)

# === 🧮 Statystyki tekstowe ===
print("\n=== Statystyki ===")
for feat in ["gene", "exon", "intron"]:
    for method in ["AUGUSTUS", "BRAKER"]:
        subset = df[(df.feature == feat) & (df.method == method)]["length"]
        if len(subset) > 0:
            print(f"{method} {feat}: n={len(subset)}, mean={statistics.mean(subset):.1f}, median={statistics.median(subset):.1f}")
print()

# === 📊 Box + Violin plots ===
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

def make_violin_box(data, x, y, title, outfile, logscale=False):
    plt.figure(figsize=(7,5))
    ax = sns.violinplot(x=x, y=y, hue="method", data=data, split=True, inner="box", cut=0)
    ax.set_title(title)
    if logscale:
        ax.set_yscale("log")
    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    plt.close()

# Długości genów, eksonów, intronów
for feat in ["gene", "exon", "intron"]:
    dsub = df[df.feature == feat]
    if not dsub.empty:
        make_violin_box(dsub, "feature", "length", f"{feat.capitalize()} length comparison", f"{feat}_length_violin.png", logscale=True)

# Egzony na gen, izoformy na gen
for feat in ["exons_per_gene", "transcripts_per_gene"]:
    dsub = dfc[dfc.feature == feat]
    if not dsub.empty:
        make_violin_box(dsub, "feature", "count", f"{feat.replace('_',' ').capitalize()} comparison", f"{feat}_violin.png", logscale=False)

print("✅ Wygenerowano wykresy PNG:")
print("   gene_length_violin.png")
print("   exon_length_violin.png")
print("   intron_length_violin.png")
print("   exons_per_gene_violin.png")
print("   transcripts_per_gene_violin.png")
