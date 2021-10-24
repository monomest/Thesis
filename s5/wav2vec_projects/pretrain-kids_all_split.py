# pretrain-kids_all.py
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
# For reading wav files
import soundfile as sf

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#       Setting duration limits
# ------------------------------------------
print("\n ------> Setting duration limits -------------------------------------\n")
lim_up = 15.5
lim_low = 0.5
print("Remove files shorter than", lim_low, " and higher than", lim_up)

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing all pretrain files
fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_all.csv"

print("Input files:", fp_all)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_manifest.csv"
myST_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_myST.csv"
CU_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_CU.csv"
OGI_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_OGI.csv"
TLT_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_TLT.csv"
native_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_native.csv"

out_list = [out_fp, myST_fp, CU_fp, OGI_fp, TLT_fp, native_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")

# All data
df = pd.read_csv(fp_all)
df["duration"] = df["duration"].apply(pd.to_numeric)

# ------------------------------------------
#  Removing rows outside duration limit
# ------------------------------------------
print("\n------> Removing rows outside duration limit... ----------------------\n")
df = df.drop(df[df.duration < lim_low].index)
df = df.drop(df[df.duration > lim_up].index)

# ------------------------------------------
#    Splitting into datasets
# ------------------------------------------
print("\n------> Splitting... -------------------------------------------------\n")
myST = df[(df['dataset'] == "myST")]
CU = df[(df['dataset'] == "CU")]
OGI = df[(df['dataset'] == "OGI")]
TLT = df[(df['dataset'] == "TLT")]
native = df[(df['dataset'] != "TLT")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
df.to_csv(out_fp,index=False)
myST.to_csv(myST_fp, index=False)
CU.to_csv(CU_fp, index=False)
OGI.to_csv(OGI_fp, index=False)
TLT.to_csv(TLT_fp, index=False)
native.to_csv(native_fp, index=False)

for filepath in out_list:
    print("Saved:", filepath)
print("Done!")

