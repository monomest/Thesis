# pretrain-kids_manifest.py
# Purpose: Create manifest file for
#          the kids pretraining data 
#          for Thesis C
# Author: Renee Lu, 2021

# ------------------------------------------
#          Information
# ------------------------------------------
# train.tsv

# <base/path>
# <path/to/wav> <frames>

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
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Root filepath for all wav files
root_fp = "/srv/scratch/chacmod"

# Dataframe in csv containing all pretrain files
fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_manifest.csv"

print("Input files:", fp_all)

# Output file to save to
dest_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/"
filename = "train.tsv"

out_fp = dest_fp + filename

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")

# All data
df = pd.read_csv(fp_all)
filepaths = df['filepath'].tolist()

# ------------------------------------------
#     Creating manifest file
# ------------------------------------------
print("\n------> Creating manifest file... ------------------------------------\n")
with open(os.path.join(dest_fp, filename), "w") as train_f:
    print(root_fp, file=train_f)

    for fname in filepaths:
        frames = sf.info(fname).frames
        file_path = fname.replace("/srv/scratch/chacmod/", "")
        print(
            "{}\t{}".format(file_path, frames), file=train_f
        )

print("Saved manifest at", out_fp)
print("Done!")

