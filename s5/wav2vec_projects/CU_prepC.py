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
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
fp_filepaths = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/cu_all_files.txt"
print("Input files:", fp_filepaths)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/CU_local/THESIS_C/CU_data_pretrain.csv"

# ------------------------------------------
#         Reading files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
df = pd.read_csv(fp_filepaths, sep="\n",
                     names=['filepath'], header=None, dtype=str)
print(df)

# ------------------------------------------
#          Data checks
# ------------------------------------------
# Flag rows where .wav file not readable
# i.e. set usable = False
#print("\n------> Flagging rows where wav file not readable\n")
#unreadable = [
#               "/srv/scratch/chacmod/CU_2/corpus/data/train-part1-cu/CC-01-20-02090/CC-01-20-02090-01544-01-0.wav",
#               "/srv/scratch/chacmod/CU_2/corpus/data/train-part1-cu/CC-04-05-01205/CC-04-05-01205-99999-01-0.wav",
#               "/srv/scratch/chacmod/CU_2/corpus/data/train-part1-cu/CC-01-06-00036/CC-01-06-00036-90002-01-0.wav",
#               "/srv/scratch/chacmod/CU_2/corpus/data/train-part1-cu/CC-02-12-00312/CC-02-12-00312-95002-01-0.wav",
#               "/srv/scratch/chacmod/CU_2/corpus/data/train-part1-cu/CC-01-13-02203/CC-01-13-02203-05125-01-0.wav"]
#df['usable'] = np.where(df['filepath'].isin(unreadable), False, True)
#print("has_audio_file = False")
#filepaths_list = df['filepath'].tolist()
#fileExists = [os.path.isfile(fp) if fp == fp else False for fp in filepaths_list]
#df['has_audio_file'] = fileExists


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


