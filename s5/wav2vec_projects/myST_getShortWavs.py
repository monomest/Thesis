# myST_getShortWavs.py
# Purpose: Only keeps wav files less than x seconds
#          from the MyST corpus.
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
# Dataframe in csv containing all the myST information
myST_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_dataframe.csv"
# File to store csv dataframe of output
myST_shorten_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_shorten_dataframe.csv"

# ------------------------------------------
#         Setting duration limit
# ------------------------------------------
print("\n------> Setting duration limit... ------------------------------------ \n")
# Read the myST csv file as dataframe, and as string type
myST_df = pd.read_csv(myST_fp, dtype=str)
# Convert duration column to float64
myST_df["duration"] = myST_df["duration"].apply(pd.to_numeric)
# Get the list of durations for all audio files
duration = myST_df['duration']
# Maximum seconds
limit = 31
#limit = max(duration)
print("--> Files limited to less than", limit, "seconds.")

# ------------------------------------------
#      Keeping x seconds or less
# ------------------------------------------
print("\n------> Keeping only short audio files... ---------------------------- \n")
# Remove all rows with duration > 8 seconds
myST_shorten_df = myST_df[myST_df.duration < limit]
print("myST_shorten:\n")
print(myST_shorten_df.head(5))
# Save dataframe with short duration into csv
myST_shorten_df.to_csv(myST_shorten_fp, index=False)
print("SUCCESS: Saved myST dataframe with only audio less than",
      limit, "seconds at",
      myST_shorten_fp)
tot_hours = sum(myST_shorten_df['duration'].tolist())/(60*60)
print("Total hours:", tot_hours)
print("Dataframe length:", len(myST_shorten_df))

