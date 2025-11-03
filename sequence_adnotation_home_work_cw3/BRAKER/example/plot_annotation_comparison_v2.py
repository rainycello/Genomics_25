#!/usr/bin/env python3
import os
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib.ticker import LogLocator, ScalarFormatter

# ============================================================
# 🧬 Genomics_25 – Annotation Comparison Visualization (safe)
# ============================================================

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

# === Helpers ===
def read_lengths(file_path):
    data = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        data.append(int(parts[3]))
                    except ValueError:
                        continue
    return data

def read_counts(file_path):
    data = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    try:
                        data.append(int(parts[0]))
                    except ValueError:
                        continue
    return data

# === Load all data ===
frames = []
for feature, methods in FILES.items():
    for method, path in methods.items():
        vals = read_lengths(path)
        if len(vals) == 0:
            print(f"[WARN] No data found in {path}")
        for v in vals:
            frames.append({"feature": feature, "method": method, "length": v})

if len(frames) == 0:
    print("❌ No data loaded! Check your .tsv files and rerun.")
    exit(1)

df = pd.DataFrame(frames)
print(f"✅ Loaded {len(df)} entries for gene/exon/intron lengths.\n")

# === Per-gene counts ===
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

# === Stats ===
print("=== Statystyki ===")
for feat in ["gene", "exon", "intron"]:
    for method in ["AUGUSTUS", "BRAKER"]:
        subset = df[(df["feature"] == feat) & (df["method"] == method)]["length"]
        if len(subset) > 0:
            print(f"{method} {feat}: n={len(subset)}, mean={statistics.mean(subset):.1f}, median={statistics.median(subset):.1f}")
        else:
            print(f"{method} {feat}: brak danych")
print()

sns.set(style="whitegrid", palette="muted", font_scale=1.2)
os.makedirs("results", exist_ok=True)

# === Plot functions ===

def make_violin(data, y, title, outfile, logscale=False):
    plt.figure(figsize=(9,6))
    ax = sns.violinplot(
        data=data,
        x="method",
        y=y,
        palette="Set2",
        inner="quart",
        cut=0,
        linewidth=1.1
    )
    ax.set_title(title, fontsize=15, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Length (bp)" if y == "length" else "Count", fontsize=13)

    if logscale:
        ax.set_yscale("log")
        # 🔹 Dodaj więcej "poznaczek" (ticków) na osi log
        ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10)*0.1, numticks=10))
        ax.yaxis.set_minor_formatter(ScalarFormatter())
    
    plt.tight_layout()
    plt.savefig(outfile, dpi=600)  # 💎 wysokiej rozdzielczości
    plt.close()


def make_box(data, y, title, outfile, logscale=False):
    plt.figure(figsize=(9,6))
    ax = sns.boxplot(
        data=data,
        x="method",
        y=y,
        palette="Set2",
        showfliers=False,    # 👁️ usuwa outliery żeby box był czytelniejszy
        width=0.6,
        linewidth=1.1
    )
    ax.set_title(title, fontsize=15, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Length (bp)" if y == "length" else "Count", fontsize=13)

    if logscale:
        ax.set_yscale("log")
        # 🔹 Dodaj więcej ticków logarytmicznych
        ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10)*0.1, numticks=10))
        ax.yaxis.set_minor_formatter(ScalarFormatter())

    plt.tight_layout()
    plt.savefig(outfile, dpi=600)  # 💎 wysokiej rozdzielczości
    plt.close()

# === Generate plots ===
for feat in ["gene", "exon", "intron"]:
    dsub = df[df["feature"] == feat]
    if not dsub.empty:
        make_violin(dsub, "length", f"{feat.capitalize()} length (violin)", f"results/{feat}_length_violin.png", logscale=True)
        make_box(dsub, "length", f"{feat.capitalize()} length (box)", f"results/{feat}_length_box.png", logscale=True)

for feat in ["exons_per_gene", "transcripts_per_gene"]:
    dsub = dfc[dfc["feature"] == feat]
    if not dsub.empty:
        make_violin(dsub, "count", f"{feat.replace('_',' ').capitalize()} (violin)", f"results/{feat}_violin.png")
        make_box(dsub, "count", f"{feat.replace('_',' ').capitalize()} (box)", f"results/{feat}_box.png")

print("\n✅ Plots saved in ./results/")
