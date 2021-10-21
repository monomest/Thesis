# myST-OGI-TLT17_combineC.py
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

print("Input files...")
fp_list = [fp_myST, fp_OGI]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/THESIS_C/myST-OGI_data_split.csv"
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/THESIS_C/myST-OGI_data_pretrain.csv"
finetune_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/THESIS_C/myST-OGI_data_finetune.csv"
dev_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/THESIS_C/myST-OGI_data_dev.csv"
test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/THESIS_C/myST-OGI_data_test.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/THESIS_C/myST-OGI_data_ignore.csv"

output_fp = [out_fp, pretrain_fp, finetune_fp, dev_fp, test_fp, ignore_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
# All data
myST_df = pd.read_csv(fp_myST)
OGI_df = pd.read_csv(fp_OGI)

# ------------------------------------------
#         Combining datasets
# ------------------------------------------
print("\n------> Combining datasets... ----------------------------------------\n")
# ---------|---------------------|-----|
# filepath | transcription_clean | set |
# ---------|---------------------|-----|

myST_df_short = myST_df[["filepath", "transcription_clean","duration","set"]]
OGI_df_short = OGI_df[["filepath", "transcription_clean","duration","set"]]
combined_df = pd.concat([myST_df_short, OGI_df_short])

# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")
# Creating set dataframes
pretrain = combined_df[(combined_df['set'] == "pretrain")]
finetune = combined_df[(combined_df['set'] == "finetune")]
dev = combined_df[(combined_df['set'] == "dev")]
test = combined_df[(combined_df['set'] == "test")]
ignore = combined_df[(combined_df['set'] == "ignore")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
combined_df.to_csv(out_fp,index=False)
pretrain.to_csv(pretrain_fp, index=False)
finetune.to_csv(finetune_fp, index=False)
dev.to_csv(dev_fp, index=False)
test.to_csv(test_fp, index=False)
ignore.to_csv(ignore_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")

