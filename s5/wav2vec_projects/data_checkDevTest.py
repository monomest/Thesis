# ---------------------------------------------------------
# data_prep.py
# Purpose: Check if speakers in Mostafa's dev/test split of data 
#          appear in my training set.
# Author: Renee Lu, 2021
# ---------------------------------------------------------

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For counting for duplicates
import collections
from collections import Counter
# For dataframes
import pandas as pd
# For regex
import re
# For checking files
import os.path
# For dealing with audio files
import soundfile as sf
# For file system related methods
from pathlib import PurePath
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#          Setting file paths
# ------------------------------------------

# Paths to Mostafa's set
m_dev_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_dev_wav.csv"
m_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_test_wav.csv"
# Path to my training set
train_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_train_15.csv"

# Output csv file
outcsv_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_devtest_in_train.csv"

# ------------------------------------------
#    Reading in csv
# ------------------------------------------
print("\n------> Reading in csv files... --------------------------------------\n")
def readCSV(fp):
    # Read the OGI csv file as dataframe, and as string type
    df = pd.read_csv(fp, dtype=str)
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df
m_dev = readCSV(m_dev_fp)
m_test = readCSV(m_test_fp)
train = readCSV(train_fp)

# ------------------------------------------
#   Get list of unique speakers 
# ------------------------------------------
print("\n------> Getting list of unique speakers... ---------------------------\n")
m_dev_spkrs = m_dev['spkr_id'].unique()
m_test_spkrs = m_test['spkr_id'].unique()
train_spkrs = train['spkr_id'].unique()

# ------------------------------------------
#   Keep speakers that appear in train
# ------------------------------------------
print("\n------> Getting list of dev and test speakers that appear in training ...\n")
dev_spkrs_double = [spkr for spkr in m_dev_spkrs if spkr in train_spkrs]
test_spkrs_double = [spkr for spkr in m_test_spkrs if spkr in train_spkrs]

# Keep only rows in dataframe that are double ups with train set
m_dev = m_dev[m_dev['spkr_id'].isin(dev_spkrs_double)]
m_dev['set']='dev'
m_test = m_test[m_test['spkr_id'].isin(test_spkrs_double)]
m_test['set']='test'

# Concat the two dev and test frames
frames = [m_dev, m_test]
doubles = pd.concat(frames)

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
print("\n------> Saving dataframe to csv file... ------------------------------\n")
doubles.to_csv(outcsv_fp,index=False)
print("SUCCESS: Saved dataframe to csv file", outcsv_fp)
print("Dataframe length:", len(doubles))
