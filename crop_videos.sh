#!/bin/bash
#SBATCH --partition=batch
#SBATCH --cpus-per-task=24
#SBATCH --mem=40G
#SBATCH --time=1-0:0:0

python crop_videos.py
