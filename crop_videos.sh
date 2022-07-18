#!/bin/bash
#SBATCH --partition=batch
#SBATCH --cpus-per-task=24
#SBATCH --mem=40G
#SBATCH --time=1-00:0:0
source ../our_virtual_envs/dlc/venv/bin/activate
python crop_videos.py
