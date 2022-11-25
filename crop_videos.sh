#!/bin/bash
#SBATCH --partition=batch
#SBATCH --cpus-per-task=24
#SBATCH --mem=24G
#SBATCH --time=1-00:0:0
source ../our_virtual_envs/dlc/venv/bin/activate
python extract_dataset_videos.py
#crop_videos.py

# --partition=batch
# --cpus-per-task=24