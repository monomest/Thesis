# pretrain-kids_combineC.py
# Purpose: Combine the kids pretraining data 
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
# Dataframe in csv containing all the data information
fp_myST = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_pretrain_unk.csv"
fp_TLT17 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17_data_pretrain.csv"
fp_TLT1618 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data_pretrain.csv"
fp_OGI = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_pretrain.csv"
fp_CU = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_pretrain.csv"


print("Input files...")
fp_list = [fp_myST, fp_TLT17, fp_TLT1618, fp_OGI, fp_CU]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain.csv"
long_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_long.csv"
short_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_short.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_ignore.csv"

output_fp = [out_fp, long_fp, short_fp, ignore_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
# All data
myST_df = pd.read_csv(fp_myST)
myST_df['dataset'] = "myST"
TLT17_df = pd.read_csv(fp_TLT17)
TLT17_df['dataset'] = "TLT"
TLT1618_df = pd.read_csv(fp_TLT1618)
TLT1618_df['dataset'] = "TLT"
OGI_df = pd.read_csv(fp_OGI)
OGI_df['dataset'] = "OGI"
CU_df = pd.read_csv(fp_CU)
CU_df['dataset'] = "CU"

# ------------------------------------------
#         Combining datasets
# ------------------------------------------
print("\n------> Combining datasets... ----------------------------------------\n")
# ---------|---------------------|-----|
# filepath | transcription_clean | set |
# ---------|---------------------|-----|

myST_df_short = myST_df[["filepath", "duration","dataset"]]
TLT17_df_short = TLT17_df[["filepath", "duration","dataset"]]
TLT1618_df_short = TLT1618_df[["filepath", "duration","dataset"]]
OGI_df_short = OGI_df[["filepath", "duration","dataset"]]
CU_df_short = CU_df[["filepath", "duration","dataset"]]

combined_df = pd.concat([myST_df_short, TLT17_df_short,
                         TLT1618_df_short, OGI_df_short,
                         CU_df_short])

# ------------------------------------------
#       Split into length portions
# ------------------------------------------
print("\n------> Splitting into long and short files... ------\n")
def splitData(duration, limit):
    if duration <= limit:
        if duration < 1:
            split = "ignore"
        else:
            split = "short"
    else:
        split = "long"
    return split
combined_df['set'] = combined_df.apply(lambda x: splitData(x['duration'], limit), axis=1)

short_df = combined_df[(combined_df['set'] == "short")]
long_df = combined_df[(combined_df['set'] == "long")]
ignore_df = combined_df[(combined_df['set'] == "ignore")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
combined_df.to_csv(out_fp,index=False)
short_df.to_csv(short_fp, index=False)
long_df.to_csv(long_fp, index=False)
ignore_df.to_csv(ignore_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")

