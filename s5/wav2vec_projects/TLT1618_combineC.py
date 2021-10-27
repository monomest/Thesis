# TLT1618_combineC.py
# Purpose: Combine TLT17 and TLT1618 finetune data 
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
fp_TLT1618 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_finetune.csv"
fp_TLT17 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17_data_finetune.csv"

print("Input files...")
fp_list = [fp_TLT17, fp_TLT1618]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT_data_finetune.csv"

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
# All data
TLT17_df = pd.read_csv(fp_TLT17)
TLT1618_df = pd.read_csv(fp_TLT1618)

# ------------------------------------------
#         Combining datasets
# ------------------------------------------
print("\n------> Combining datasets... ----------------------------------------\n")

combined_df = pd.concat([TLT17_df, TLT1618_df])

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
combined_df.to_csv(out_fp,index=False)
print("Saved:", out_fp)

print("Done!")

