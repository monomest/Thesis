# myST_getShortWavs.py
# Purpose: Only keeps wav files less than or equal to x seconds
#          from the MyST corpus.
# Author: Renee Lu, 2021

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dealing with audio files
import soundfile as sf
# For dataframes
import pandas as pd

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
# Maximum seconds
limit = 8
print("--> Files limited to", limit, "seconds.")

# ------------------------------------------
#      Keeping x seconds or less
# ------------------------------------------
print("\n------> Keeping only short audio files... ---------------------------- \n")
# Read the myST csv file as dataframe
myST_df = pd.read_csv(myST_fp)
# Remove all rows with duration > 8 seconds
myST_shorten_df = myST_df[myST_df.duration <= limit]
print("myST_shorten:\n")
print(myST_shorten_df.head(5))
# Save dataframe with short duration into csv
myST_shorten_df.to_csv(myST_shorten_fp, index=False)
print("SUCCESS: Saved myST dataframe with only audio less than or equal to",
      limit, "seconds or less at",
      myST_shorten_fp)
tot_hours = sum(myST_shorten_df['duration'].tolist())/(60*60)
print("Total hours:", tot_hours)
print("Dataframe length:", len(myST_shorten_df))

