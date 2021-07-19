# OGI_getSpkrs.py
# Purpose: Gets the list of speakers and their
#          total audio duration from MyST corpus.
# Requirements: OGI_shorten.dataframe.csv
#               Created from OGI_getShortWavs.py
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
OGI_shorten_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_15.csv"
# File to store speaker and duration information
OGI_spkrs_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_spkrs_15.csv"

# ------------------------------------------
#          Getting list of speakers
# ------------------------------------------
print("\n------> Getting list of unique speakers and their total durations...\n")
# Read the OGI csv file as dataframe, and as string type
OGI_shorten_df = pd.read_csv(OGI_shorten_fp, dtype=str)
# Convert duration column to float64
OGI_shorten_df["duration"] = OGI_shorten_df["duration"].apply(pd.to_numeric)
# Dropping irrelevant columns
OGI_shorten_df.drop(columns=['filepath', 'transcription'], inplace=True)
# |---------|----------|
# | spkr_id | duration |
# |---------|----------|
# | ......  |    ...   |
# Group by speaker id, and then sum the durations for each speaker id
spkrs = OGI_shorten_df.groupby(["spkr_id"]).duration.sum().reset_index()

# ------------------------------------------
#           Saving to csv file
# ------------------------------------------
print("\n------> Saving information to file...\n")
# Save spkr_id as string so leading zeros are not removed
spkrs['spkr_id'] = spkrs['spkr_id'].astype('str')
spkrs.to_csv(OGI_spkrs_fp, index=False)
print("SUCCESS: Saved speaker and duration information at",
      OGI_spkrs_fp)
print("-> Total speakers:",len(spkrs))
print("-> Total hours:",spkrs['duration'].sum()/(60*60))
print("-> Description of duration:")
print(spkrs.duration.describe())

