#!/bin/bash

# Load conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base

echo "========== $(date) =========="
echo "[START] Running data ingestion..."
python data_ingestion.py

echo "[STEP] Running NLP processing..."
python nlp_processing.py

echo "[STEP] Generating daily summary report..."
python summary_report.py

echo "[STEP] Generating daily summary report..."
python app.py

echo "[DONE] Pipeline completed at $(date)"
