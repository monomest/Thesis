# myST_getSpkrs.py
# Purpose: Gets the list of speakers and their
#          total audio duration from MyST corpus.
# Requirements: myST_shorten.dataframe.csv
#               Created from myST_getShortWavs.py
# Author: Renee Lu, 2021

# ------------------------------------------
#            Importing Libraries
# ------------------------------------------
# For dataframes
import pandas as pd

# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#             Setting file paths
# ------------------------------------------
# File storing csv dataframe of output
myST_shorten_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_shorten_dataframe_15.csv"
# File to store speaker and duration information
myST_spkrs_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_spkrs_15.csv"

# ------------------------------------------
#          Getting list of speakers
# ------------------------------------------
print("\n------> Getting list of unique speakers and their total durations...\n")
# Read the myST csv file as dataframe, and as string type
myST_shorten_df = pd.read_csv(myST_shorten_fp, dtype=str)
# Convert duration column to float64
myST_shorten_df["duration"] = myST_shorten_df["duration"].apply(pd.to_numeric)
# Dropping irrelevant columns
myST_shorten_df.drop(columns=['filepath', 'transcription'], inplace=True)
# |---------|----------|
# | spkr_id | duration |
# |---------|----------|
# | ......  |    ...   |
# Group by speaker id, and then sum the durations for each speaker id
spkrs = myST_shorten_df.groupby(["spkr_id"]).duration.sum().reset_index()

# ------------------------------------------
#           Saving to csv file
# ------------------------------------------
print("\n------> Saving information to file...\n")
# Save spkr_id as string so leading zeros are not removed
spkrs['spkr_id'] = spkrs['spkr_id'].astype('str')
spkrs.to_csv(myST_spkrs_fp, index=False)
print("SUCCESS: Saved speaker and duration information at",
      myST_spkrs_fp)
print("-> Total speakers:",len(spkrs))
print("-> Total hours:",spkrs['duration'].sum()/(60*60))
print("-> Description of duration:")
print(spkrs.duration.describe())

