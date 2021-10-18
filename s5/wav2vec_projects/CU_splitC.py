# CU_prepC.py
# Purpose: Prep the CU data 
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
# Setting maximum seconds duration
# ------------------------------------------
print("\n------> Setting duration limit... ------------------------------------ \n")
# Maximum seconds
limit = 15
print("--> Long files flagged as those greater than", limit, "seconds.")

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data.csv"
print("Input files:", fp_all)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_split.csv"
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_pretrain.csv"
pretrain_short_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_pretrain_short.csv"
pretrain_long_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_pretrain_long.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_ignore.csv"

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


