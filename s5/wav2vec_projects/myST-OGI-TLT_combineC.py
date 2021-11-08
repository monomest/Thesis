# myST-OGI-TLT_combineC.py
# Purpose: Split the transcribed myST data 
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

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing all the data information
fp_myST = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_split.csv"
fp_OGI = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_split.csv"
fp_TLT = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT_data_finetune.csv"

print("Input files...")
fp_list = [fp_myST, fp_OGI, fp_TLT]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT17_local/THESIS_C/myST-OGI-TLT_data_split.csv"
finetune_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT17_local/THESIS_C/myST-OGI-TLT_data_finetune.csv"

output_fp = [out_fp, finetune_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
# All data
myST_df = pd.read_csv(fp_myST)
OGI_df = pd.read_csv(fp_OGI)
TLT_df = pd.read_csv(fp_TLT)

# ------------------------------------------
#         Combining datasets
# ------------------------------------------
print("\n------> Combining datasets... ----------------------------------------\n")
# ---------|---------------------|-----|
# filepath | transcription_clean | set |
# ---------|---------------------|-----|

myST_df_short = myST_df[["filepath", "transcription_clean","duration","set"]]
OGI_df_short = OGI_df[["filepath", "transcription_clean","duration", "set"]]
TLT_df_short = TLT_df[["filepath", "transcription_clean","duration", "set"]]
combined_df = pd.concat([myST_df_short, OGI_df_short, TLT_df_short])

# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")
# Creating set dataframes
finetune = combined_df[(combined_df['set'] == "finetune")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
combined_df.to_csv(out_fp,index=False)
finetune.to_csv(finetune_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")

