# myST_splitC_unk.py
# Purpose: Split the transcribed myST data 
#          for Thesis C with <UNK> tags
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
fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_split_unk.csv"

print("Input files...")
fp_list = [fp_all]
for fp in fp_list:
    print(fp)

# Output file to save to
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_unk_pretrain.csv"
finetune_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_unk_finetune.csv"
dev_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_unk_dev.csv"
test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_unk_test.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_unk_ignore.csv"

output_fp = [pretrain_fp, finetune_fp, dev_fp, test_fp, ignore_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
def readCSV(fp):
    # Read the csv file as dataframe, and as string type 
    # so that speaker IDs retain leading zeros
    df = pd.read_csv(fp, dtype={'spkr_id': object})
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df

# All data
myST_df = readCSV(fp_all)

# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")

# Creating set dataframes
myST_pretrain = myST_df[(myST_df['set'] == "pretrain")]
myST_finetune = myST_df[(myST_df['set'] == "finetune")]
myST_dev = myST_df[(myST_df['set'] == "dev")]
myST_test = myST_df[(myST_df['set'] == "test")]
myST_ignore = myST_df[(myST_df['set'] == "ignore")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
myST_pretrain.to_csv(pretrain_fp, index=False)
myST_finetune.to_csv(finetune_fp, index=False)
myST_dev.to_csv(dev_fp, index=False)
myST_test.to_csv(test_fp, index=False)
myST_ignore.to_csv(ignore_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")

