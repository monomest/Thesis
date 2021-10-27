# data_gadiC.py
# Purpose: Prep the data for gadi
#          for Thesis C
# Author: Renee Lu, 2021

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dataframes
import pandas as pd
import numpy as np
# For printing filepath
import os
# For reading files
from pathlib import Path
# For regex
import re
# For dealing with audio files
import soundfile as sf

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Filepaths for OGI
fp_OGI_10h = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_10h_light.csv"
fp_OGI_10min = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_10min_light.csv"
fp_OGI_1h = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_1h_light.csv"
fp_OGI_5h = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_5h_light.csv"
fp_OGI = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_light.csv"
fp_OGI_dev = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_dev_short_light.csv"

# Filepaths for TLT
fp_TLT = "/scratch/wa66/rl4201/Thesis/s5/TLT_local/THESIS_C/TLT_data_finetune_light.csv"

fp_OGI_list = [fp_OGI_10h, fp_OGI_10min, fp_OGI_1h, fp_OGI_5h, fp_OGI, fp_OGI_dev]
print("Input files:")
for fp in fp_OGI_list:
    print(fp)
print(fp_TLT)

# Output file to save to
out_OGI_10h = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_10h_light_gadi.csv"
out_OGI_10min = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_10min_light_gadi.csv"
out_OGI_1h = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_1h_light_gadi.csv"
fp_OGI_5h = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_5h_light.csv"
fp_OGI = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_finetune_light.csv"
fp_OGI_dev = "/scratch/wa66/rl4201/Thesis/s5/OGI_local/THESIS_C/OGI_data_dev_short_light.csv"
fp_TLT = "/scratch/wa66/rl4201/Thesis/s5/TLT_local/THESIS_C/TLT_data_finetune_light.csv"

fp_OGI_list = [fp_OGI_10h, fp_OGI_10min, fp_OGI_1h, fp_OGI_5h, fp_OGI, fp_OGI_dev]











out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_split.csv"
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_pretrain.csv"
pretrain_short_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_pretrain_short.csv"
pretrain_long_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_pretrain_long.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_ignore.csv"

output_list = [out_fp, pretrain_fp, pretrain_short_fp,
               pretrain_long_fp, ignore_fp]

# ------------------------------------------
#         Reading files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
df = pd.read_csv(fp_all)
# Convert duration column to float64
df['duration'] = df['duration'].apply(pd.to_numeric)

# ------------------------------------------
#           Getting usable files
# ------------------------------------------
df['usable'] = True
df.loc[(df.duration != df.duration),'usable'] = False

# ------------------------------------------
#              Splitting
# ------------------------------------------
print("\n------> Splitting files... ------------------------------------\n")

def splitData(usable, duration, limit):
    if usable != True:
        split = "ignore"
    else:
        if duration <= limit:
            split = "short"
        else:
            split = "long"
    return split
df['set'] = df.apply(lambda x: splitData(x['usable'],
                            x['duration'], limit), axis=1)

# Creating set dataframes
pretrain_df = df[((df['set'] == "short") | (df['set'] == "long"))]
short_df = df[(df['set'] == "short")]
long_df = df[(df['set'] == "long")]
ignore_df = df[(df['set'] == "ignore")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
df.to_csv(out_fp,index=False)
pretrain_df.to_csv(pretrain_fp, index=False)
short_df.to_csv(pretrain_short_fp, index=False)
long_df.to_csv(pretrain_long_fp, index=False)
ignore_df.to_csv(ignore_fp, index=False)

for fp in output_list:
    print("Saved:", fp)


