#!/bin/bash
set -euo pipefail

XLSX="manifests/WashU_Second_Study_baseline_EDTA_samples_CNH_QC_final copy.xlsx"
BAM_DIR="/storage1/fs1/christophermaher/Active/maherlab/netra/rawdata/FASTQ_FILES/CRC_EDTA/bam/wgs_72"
OUT="manifests/edta_wgs_sample_manifest.tsv"

python3 - << PY
import os
from openpyxl import load_workbook

xlsx = r"$XLSX"
bam_dir = r"$BAM_DIR"
out = r"$OUT"

wb = load_workbook(xlsx, data_only=True)
ws = wb["Sheet1"]

bam_ids = {os.path.splitext(f)[0] for f in os.listdir(bam_dir) if f.endswith(".bam")}

rows = []
for row in ws.iter_rows(min_row=5, values_only=True):
    sample = row[0]
    tube = row[1]
    hmc_id = row[2]
    wgs_id = row[3]

    if sample is None or wgs_id is None:
        continue

    sample = str(sample).strip()
    tube = "" if tube is None else str(tube).strip()
    hmc_id = "" if hmc_id is None else str(hmc_id).strip()
    wgs_id = str(wgs_id).strip()

    if wgs_id in bam_ids:
        bam_path = os.path.join(bam_dir, wgs_id + ".bam")
        rows.append((sample, tube, hmc_id, wgs_id, bam_path))

rows.sort(key=lambda x: x[3])

with open(out, "w") as fh:
    fh.write("sample\\ttube_type\\t5hmc_seq_id\\twgs_seq_id\\tbam_path\\n")
    for r in rows:
        fh.write("\\t".join(r) + "\\n")

print(f"Wrote {len(rows)} rows to {out}")
PY
