# OGI_separate.py
# Purpose: Separates OGI dataframe into scripted and spontaneous
# OGI Corpus:
#     - scripted
#     - spontaneous
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
OGI_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_dataframe.csv"
# File to store csv dataframe of output
OGI_scripted_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted.csv"
OGI_spontaneous_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_spontaneous.csv"

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in csv file... ------------------------------------ \n")
# Read the OGI csv file as dataframe, and as string type
OGI_df = pd.read_csv(OGI_fp, dtype=str)
# Convert duration column to float64
OGI_df["duration"] = OGI_df["duration"].apply(pd.to_numeric)

# ------------------------------------------
# Separating into scripted and spontaneous 
# ------------------------------------------
print("\n------> Separating into scripted and spontaneous... ---------------------------- \n")
# Filtering for scripted
OGI_scripted_df = OGI_df[OGI_df['filepath'].str.contains("scripted")]
# Filtering for spontaneous
OGI_spontaneous_df = OGI_df[OGI_df['filepath'].str.contains("spontaneous")]

# ------------------------------------------
#              Saving as csv
# ------------------------------------------
# Save dataframes into csv
# Scripted
# Make sure speaker ID are strings
OGI_scripted_df['spkr_id'] = OGI_scripted_df['spkr_id'].astype('str')
OGI_scripted_df.to_csv(OGI_scripted_fp, index=False)
print("SUCCESS: Saved OGI scripted dataframe at",
      OGI_scripted_fp)
print("Num utterances:", len(OGI_scripted_df))
print("Total hours:", OGI_scripted_df.duration.sum()/(60*60))
# Spontaneous
# Make sure speaker ID are strings
OGI_spontaneous_df['spkr_id'] = OGI_spontaneous_df['spkr_id'].astype('str')
OGI_spontaneous_df.to_csv(OGI_spontaneous_fp, index=False)
print("SUCCESS: Saved OGI spontaneous dataframe at",
       OGI_spontaneous_fp)
print("Total_hours:", OGI_spontaneous_df.duration.sum()/(60*60))
print("Num utterances:", len(OGI_scripted_df))
