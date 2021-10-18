# TLT1618_prepC.py
# Purpose: Prep the TLT1618 data 
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
fp_filepaths = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/kaldi_datafiles/untranscribed_all_files.txt"
print("Input files:", fp_filepaths)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT1618_data.csv"

# ------------------------------------------
#         Reading files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
df = pd.read_csv(fp_filepaths, sep="\n",
                     names=['filepath'], header=None, dtype=str)
print(df)

# ------------------------------------------
#      Getting duration of audio
# ------------------------------------------
# Get duration of each wav file
print("\n------> Getting duration in seconds of each wav file\n")
print("duration")
def getDuration(fp):   
    try:
        duration = len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate
    except RuntimeError:
        duration = np.nan
    return duration
df['duration'] = df.apply(lambda x: getDuration(x['filepath']), axis=1)

print(df.duration.describe())
# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
df.to_csv(out_fp,index=False)

print("Saved:", out_fp)


