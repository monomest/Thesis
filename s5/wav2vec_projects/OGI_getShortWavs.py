# OGI_getShortWavs.py
# Purpose: Only keeps wav files less than x seconds
#          from the OGI corpus.
# Author: Renee Lu, 2021

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dealing with audio files
import soundfile as sf
# For dataframes
import pandas as pd
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
# Dataframe in csv containing all the OGI information
OGI_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted.csv"
# File to store csv dataframe of output
OGI_shorten_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_15.csv"

# ------------------------------------------
#         Setting duration limit
# ------------------------------------------
print("\n------> Setting duration limit... ------------------------------------ \n")
# Read the OGI csv file as dataframe, and as string type
OGI_df = pd.read_csv(OGI_fp, dtype=str)
# Convert duration column to float64
OGI_df["duration"] = OGI_df["duration"].apply(pd.to_numeric)
# Get the list of durations for all audio files
duration = OGI_df['duration']
# Maximum seconds
limit = 15
#limit = max(duration)
print("--> Files limited to less than", limit, "seconds.")

# ------------------------------------------
#      Keeping x seconds or less
# ------------------------------------------
print("\n------> Keeping only short audio files... ---------------------------- \n")
# Remove all rows with duration > 8 seconds
OGI_shorten_df = OGI_df[OGI_df.duration < limit]
print("OGI_shorten:\n")
print(OGI_shorten_df.head(5))
# Save dataframe with short duration into csv
OGI_shorten_df['spkr_id'] = OGI_shorten_df['spkr_id'].astype('str')
OGI_shorten_df.to_csv(OGI_shorten_fp, index=False)
print("SUCCESS: Saved OGI dataframe with only audio less than",
      limit, "seconds at",
      OGI_shorten_fp)
tot_hours = sum(OGI_shorten_df['duration'].tolist())/(60*60)
print("Total hours:", tot_hours)
print("Dataframe length:", len(OGI_shorten_df))

