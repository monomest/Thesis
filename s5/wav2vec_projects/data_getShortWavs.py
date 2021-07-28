# data_getShortWavs.py
# Purpose: Only keeps wav files less than x seconds
#          from the dataset corpus.
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
print("\n------> Setting filepaths... -----------------------------------------\n")

#dataset_name = "myST"
dataset_name = "OGI"
print("dataset_name:", dataset_name)

# File name of where dataset information is stored as csv
#dataset_filename = "myST_dataframe"
dataset_filename = "OGI_scripted"
print("dataset_filename:", dataset_filename)

# Where to store csv dataframes of output
#shorten_filename = "myST_dataframe_shorten_15"
shorten_filename = "OGI_scripted_15"
print("shorten_filename:", shorten_filename)

# Base filepath
base_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/" + dataset_name + "_local/"

# ------------------------------------------
#       Setting duration limit
# ------------------------------------------
# Setting maximum seconds duration
print("\n------> Setting duration limit... ------------------------------------ \n")
# Maximum seconds
limit = 15
print("--> Files limited to less than", limit, "seconds.")

# ------------------------------------------
#           Generating file paths
# ------------------------------------------
# Dataframe in csv containing all the data information
data_fp = base_fp + dataset_filename + ".csv"
# File to store csv dataframe of output
data_shorten_fp = base_fp + shorten_filename + ".csv"

# ------------------------------------------
#      Keeping x seconds or less
# ------------------------------------------
print("\n------> Keeping only short audio files... ---------------------------- \n")
# Remove all rows with duration > 8 seconds
data_shorten_df = data_df[data_df.duration < limit]
print("data_shorten:\n")
print(data_shorten_df.head(5))
# Save dataframe with short duration into csv
data_shorten_df['spkr_id'] = data_shorten_df['spkr_id'].astype('str')
data_shorten_df.to_csv(data_shorten_fp, index=False)
print("SUCCESS: Saved dataset dataframe with only audio less than",
      limit, "seconds at",
      data_shorten_fp)
tot_hours = sum(data_shorten_df['duration'].tolist())/(60*60)
print("Total hours:", tot_hours)
print("Dataframe length:", len(data_shorten_df))

