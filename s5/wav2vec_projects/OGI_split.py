# ---------------------------------------------------------
# OGI_split.py
# Purpose: Split OGI speech corpus into train and test.
# Requirements: OGI_dataframe.csv from OGI_prep.py
#               [optional] OGI_shorten_dataframe.csv from OGI_getShortWavs.py
#               OGI_spkrs.csv from OGI_getSpkrs.py
# Author: Renee Lu, 2021
# ---------------------------------------------------------

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For dataframes
import pandas as pd
# For splitting data
from sklearn.model_selection import train_test_split
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#     Setting train and test portions
# ------------------------------------------
print("\n------> Setting train and test portions ------------------------------\n")
# Set as a fraction e.g. 0.5 = 50% of data
num_test = 0.02
num_train = 1-num_test
print("--> Splitting as train:", num_train, "and test:", num_test)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# File path to OGI dataframe csv file,
# generated from OGI_prep.py and/or
# OGI_getShortWavs.py and/or OGI_separate
OGI_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_15.csv"
# Speaker information
OGI_spkrs_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_spkrs_15.csv"
# Where to save spkrs train dataframe
OGI_spkrs_train_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_spkrs_train_15.csv"
# Where to save spkrs test dataframe
OGI_spkrs_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_spkrs_test_15.csv"
# Where to save training dataframe
OGI_train_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_train_15.csv"
# Where to save testing
OGI_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted_test_15.csv"

# ------------------------------------------
#        Splitting by speakers
# ------------------------------------------
print("\n------> Splitting by speakers... -------------------------------------\n")
# Reading in OGI dataframe from csv file, as string type
# to preserve leading zeros in speaker id
OGI_df = pd.read_csv(OGI_fp, dtype=str)
# Converting duration column to float64
OGI_df["duration"] = OGI_df["duration"].apply(pd.to_numeric)
# Reading in speakers dataframe from csv file, as string type
# to preserve leading zeros in speaker id
spkrs_df = pd.read_csv(OGI_spkrs_fp, dtype=str)
# Converting duration column to float64
spkrs_df["duration"] = spkrs_df["duration"].apply(pd.to_numeric)

# Split into train and test by speakers
train_spkrs, test_spkrs = train_test_split(spkrs_df, test_size=num_test, random_state=6, shuffle=True)
print("--> Speakers in train:", len(train_spkrs))
print("--> Hours in train:", train_spkrs['duration'].sum()/(60*60))
print("--> Proportion of train:", (train_spkrs['duration'].sum()/(60*60))/(spkrs_df['duration'].sum()/(60*60)))
print("--> Speakers in test:", len(test_spkrs))
print("--> Hours in test:", test_spkrs['duration'].sum()/(60*60))
print("--> Proportion of test:", (test_spkrs['duration'].sum()/(60*60))/(spkrs_df['duration'].sum()/(60*60)))
# Convert spkrs dataframes to csv
# Also save speaker id as string so leading zeros remain
train_spkrs.to_csv(OGI_spkrs_train_fp, index=False)
test_spkrs.to_csv(OGI_spkrs_test_fp, index=False)
print("SUCCESS: Saved train and test spkrs in",
      OGI_spkrs_train_fp, "and",
      OGI_spkrs_test_fp)

# ------------------------------------------
#      Splitting into train and test
# ------------------------------------------
print("\n------> Splitting into train and test... -----------------------------\n")
# Use isin() to filter OGI dataframe by speakers appearing in train & test dataframe
train_spkrs_list = train_spkrs.drop(columns='duration')
#print("Train_spkrs:",train_spkrs.head())
keys_train = list(train_spkrs_list.columns.values)
all_spkrs_index = OGI_df.set_index(keys_train).index
train_spkrs_index = train_spkrs_list.set_index(keys_train).index
# Get all the train rows i.e. speakers in train speakers
train_df = OGI_df[all_spkrs_index.isin(train_spkrs_index)]
#print("train_df:",train_df.head())
# Get all the test rows i.e. speakers NOT in train speakers
test_df = OGI_df[~all_spkrs_index.isin(train_spkrs_index)]
#print("test_df",test_df.head())

# ------------------------------------------
#          Saving to csv files
# ------------------------------------------
# Drop the spkr_id column because not needed
train_df.drop(columns=['spkr_id'], inplace=True)
test_df.drop(columns=['spkr_id'], inplace=True)
# Save as csv file
train_df.to_csv(OGI_train_fp, index=False)
test_df.to_csv(OGI_test_fp, index=False)
print("SUCCESS: Created train and test portions in",
      OGI_train_fp, "and", OGI_test_fp)
train_hours = sum(train_df['duration'].tolist())/(60*60)
test_hours = sum(test_df['duration'].tolist())/(60*60)
print("Train files:", len(train_df),
      "| Train hours:", train_hours)
print("Test files:", len(test_df),
      "| Test hours:", test_hours)
