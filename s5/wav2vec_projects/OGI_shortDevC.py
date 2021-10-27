# OGI_shortDevC.py
# Purpose: Get short dev files only 
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
# For dealing with NaN
import math

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing all the data information
# Mostafa's split
fp_dev = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_dev.csv"

print("Input file:", fp_dev)
# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_dev_short.csv"

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

# Get the dataframes of files that will be used
dev_df = readCSV(fp_dev)

dev_df = dev_df[(dev_df['duration'] <= 15)]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
dev_df.to_csv(out_fp,index=False)

print("Saved:", out_fp)

print("Done!")



