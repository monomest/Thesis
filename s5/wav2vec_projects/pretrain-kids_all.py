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
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing long files and corresponding shorter split wav files
fp_long = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_split_list.csv"
# Dataframe in csv containing short files
fp_short = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_short.csv"

print("Input files...")
fp_list = [fp_long, fp_short]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_all.csv"

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")

# All data
long_df = pd.read_csv(fp_long, converters={'split_files': pd.eval})
long_df = long_df.drop(columns=['duration', 'filepath', 'set'])
long_df = long_df.rename(columns={"split_files": "filepath"})
short_df = pd.read_csv(fp_short)
short_df = short_df.drop(columns=['set'])
short_df["duration"] = short_df["duration"].apply(pd.to_numeric)

# ------------------------------------------
#         Combining datasets
# ------------------------------------------
print("\n------> Combining datasets... ----------------------------------------\n")
# ---------|----------|---------|
# filepath | duration | dataset |
# ---------|----------|---------|

# Remove all rows with empty lists and then explode
long_df = long_df[long_df['filepath'].map(lambda d: len(d)) > 0]
long_df = long_df.explode('filepath')

# Get duration of each wav file
print("\n------> Getting duration in seconds of each split wav file\n")
print("duration")
def getDuration(fp):
    duration = len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate
    return duration
long_df['duration'] = long_df.apply(lambda x: getDuration(x['filepath']), axis=1)

# Combine dataframes
combined_df = pd.concat([short_df, long_df], ignore_index=True)

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
combined_df.to_csv(out_fp,index=False)
print("Saved:", out_fp)
print("Done!")

