# ---------------------------------------------------------
# myST_split.py
# Purpose: Split MyST speech corpus into train and test.
# Requirements: myST_dataframe.csv from myST_prep.py
#               [optional] myST_shorten_dataframe.csv from myST_getShortWavs.py
#               myST_spkrs.csv from myST_getSpkrs.py
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
num_test = 0.3
num_train = 1-num_test
print("--> Splitting as train:", num_train, "and test:", num_test)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# File path to MyST dataframe csv file,
# generated from myST_prep.py and/or
# myST_getShortWavs.py
myST_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_shorten_dataframe.csv"
# Speaker information
myST_spkrs_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_spkrs.csv"
# Where to save spkrs train dataframe
myST_spkrs_train_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_spkrs_train.csv"
# Where to save spkrs test dataframe
myST_spkrs_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_spkrs_test.csv"
# Where to save training dataframe
myST_train_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_train.csv"
# Where to save testing
myST_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_test.csv"

# ------------------------------------------
#        Splitting by speakers
# ------------------------------------------
print("\n------> Splitting by speakers... -------------------------------------\n")
# Reading in myST dataframe from csv file, as string type
# to preserve leading zeros in speaker id
myST_df = pd.read_csv(myST_fp, dtype=str)
# Converting duration column to float64
myST_df["duration"] = myST_df["duration"].apply(pd.to_numeric)
# Reading in speakers dataframe from csv file, as string type
# to preserve leading zeros in speaker id
spkrs_df = pd.read_csv(myST_spkrs_fp, dtype=str)
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
train_spkrs.to_csv(myST_spkrs_train_fp, index=False)
test_spkrs.to_csv(myST_spkrs_test_fp, index=False)
print("SUCCESS: Saved train and test spkrs in",
      myST_spkrs_train_fp, "and",
      myST_spkrs_test_fp)

# ------------------------------------------
#      Splitting into train and test
# ------------------------------------------
print("\n------> Splitting into train and test... -----------------------------\n")
# Use isin() to filter myST dataframe by speakers appearing in train & test dataframe
train_spkrs_list = train_spkrs.drop(columns='duration')
#print("Train_spkrs:",train_spkrs.head())
keys_train = list(train_spkrs_list.columns.values)
all_spkrs_index = myST_df.set_index(keys_train).index
train_spkrs_index = train_spkrs_list.set_index(keys_train).index
# Get all the train rows i.e. speakers in train speakers
train_df = myST_df[all_spkrs_index.isin(train_spkrs_index)]
#print("train_df:",train_df.head())
# Get all the test rows i.e. speakers NOT in train speakers
test_df = myST_df[~all_spkrs_index.isin(train_spkrs_index)]
#print("test_df",test_df.head())

# ------------------------------------------
#          Saving to csv files
# ------------------------------------------
# Save spkr_id as string so leading zeros are not removed
train_df['spkr_id'] = train_df['spkr_id'].astype('str')
test_df['spkr_id'] = test_df['spkr_id'].astype('str')
# Save as csv file
train_df.to_csv(myST_train_fp, index=False)
test_df.to_csv(myST_test_fp, index=False)
print("SUCCESS: Created train and test portions in",
      myST_train_fp, "and", myST_test_fp)
train_hours = sum(train_df['duration'].tolist())/(60*60)
test_hours = sum(test_df['duration'].tolist())/(60*60)
print("Train files:", len(train_df),
      "| Train hours:", train_hours)
print("Test files:", len(test_df),
      "| Test hours:", test_hours)
