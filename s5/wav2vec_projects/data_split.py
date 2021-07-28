# ---------------------------------------------------------
# data_split.py
# Purpose: Split speech corpus into train, dev and test sets.
#          Splits by speakers to ensure no speaker appears in two
#          different sets.
# Requirements: Ran prep.py
#               [optional] Ran getShortWavs.py
#               Ran getSpkrs.py
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
num_train = 0.70
num_dev = 0.15
num_test = 0.15
print("--> Splitting as train:", num_train, "and dev:",
     num_dev, "and test:", num_test)

# ------------------------------------------
#           Setting seed
# ------------------------------------------
print("\n------> Setting seed... ----------------------------------------------\n")
# Set a seed to ensure random split can be reproducible
seed = 6
print("--> Setting seed as:", seed)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# Information for dataframe csv file
# created by prep.py or getShortWavs.py
dataset_name = "OGI"
#dataset_name = "myST"
dataset_filename = "OGI_scripted_15"
#dataset_filename = "myST_shorten_dataframe_15"
# Speakers csv file
spkrs_filename = "OGI_scripted_spkrs_15"
#spkrs_filename = "myST_spkrs_15"

# Where to save spkrs train, dev and test information
spkrs_train_filename = "OGI_scripted_spkrs_train_15"
#spkrs_train_filename = "myST_spkrs_train_15-test"
spkrs_dev_filename = "OGI_scripted_spkrs_dev_15"
#spkrs_dev_filename = "myST_spkrs_dev_15-test"
spkrs_test_filename = "OGI_scripted_spkrs_test_15"
#spkrs_test_filename = "myST_spkrs_test_15-test"

# Where to save train, dev and test dataframes as csv
train_filename = "OGI_scripted_train_15"
#train_filename = "myST_train_15-test"
dev_filename = "OGI_scripted_dev_15"
#dev_filename = "myST_dev_15-test"
test_filename = "OGI_scripted_test_15"
#test_filename = "myST_test_15-test"

# base filepath
base_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/" + dataset_name + "_local/"

# ------------------------------------------
#       Generating filepaths
# ------------------------------------------
# File path to dataframe csv file,
data_fp = base_fp + dataset_filename + ".csv"
# Speaker information
data_spkrs_fp = base_fp + spkrs_filename + ".csv"
# Where to save spkrs train dataframe
data_spkrs_train_fp = base_fp + spkrs_train_filename + ".csv"
# Where to save spkrs dev dataframe
data_spkrs_dev_fp = base_fp + spkrs_dev_filename + ".csv"
# Where to save spkrs test dataframe
data_spkrs_test_fp = base_fp + spkrs_test_filename + ".csv"
# Where to save training dataframe
data_train_fp = base_fp + train_filename + ".csv"
# Where to save development dataframe
data_dev_fp = base_fp + dev_filename + ".csv"
# Where to save testing dataframe
data_test_fp = base_fp + test_filename + ".csv"

# ------------------------------------------
#        Reading in dataframes
# ------------------------------------------
print("\n------> Reading in dataframes... -------------------------------------\n")
# Reading in data dataframe from csv file, as string type
# to preserve leading zeros in speaker id
data_df = pd.read_csv(data_fp, dtype=str)
# Converting duration column to float64
data_df["duration"] = data_df["duration"].apply(pd.to_numeric)
# Reading in speakers dataframe from csv file, as string type
# to preserve leading zeros in speaker id
spkrs_df = pd.read_csv(data_spkrs_fp, dtype=str)
# Converting duration column to float64
spkrs_df["duration"] = spkrs_df["duration"].apply(pd.to_numeric)

# ------------------------------------------
#        Splitting by speakers
# ------------------------------------------
print("\n------> Splitting by speakers... -------------------------------------\n")
# Split into train and combined dev_test by speakers
num_dev_test = num_dev + num_test
train_spkrs, dev_test_spkrs = train_test_split(spkrs_df, test_size=num_dev_test, random_state=seed, shuffle=True)
print("--> Speakers in train:", len(train_spkrs))
print("--> Hours in train:", train_spkrs['duration'].sum()/(60*60))
print("--> Proportion of train:", (train_spkrs['duration'].sum()/(60*60))/(spkrs_df['duration'].sum()/(60*60)))
# Split dev_test into dev and test
prop_test = num_test/num_dev_test
dev_spkrs, test_spkrs = train_test_split(dev_test_spkrs, test_size=prop_test, random_state=seed, shuffle=True)
print("--> Speakers in dev:", len(dev_spkrs))
print("--> Hours in dev:", dev_spkrs['duration'].sum()/(60*60))
print("--> Proportion of dev:", (dev_spkrs['duration'].sum()/(60*60))/(spkrs_df['duration'].sum()/(60*60)))
print("--> Speakers in test:", len(test_spkrs))
print("--> Hours in test:", test_spkrs['duration'].sum()/(60*60))
print("--> Proportion of test:", (test_spkrs['duration'].sum()/(60*60))/(spkrs_df['duration'].sum()/(60*60)))
# Convert spkrs dataframes to csv
# Also save speaker id as string so leading zeros remain
train_spkrs.to_csv(data_spkrs_train_fp, index=False)
dev_spkrs.to_csv(data_spkrs_dev_fp, index=False)
test_spkrs.to_csv(data_spkrs_test_fp, index=False)
print("SUCCESS: Saved train spkrs in",
      data_spkrs_train_fp, "and dev spkrs in",
      data_spkrs_dev_fp, "and test spkrs in",
      data_spkrs_test_fp)

# ------------------------------------------
#      Splitting into train and test
# ------------------------------------------
print("\n------> Splitting into train and test... -----------------------------\n")
# Use isin() to filter data dataframe by speakers appearing in train, dev & test dataframe

# Filter for train set
train_spkrs_list = train_spkrs.drop(columns='duration')
keys_train = list(train_spkrs_list.columns.values)
all_spkrs_index = data_df.set_index(keys_train).index
train_spkrs_index = train_spkrs_list.set_index(keys_train).index
# Get all the train rows i.e. speakers in train speakers
train_df = data_df[all_spkrs_index.isin(train_spkrs_index)]

# Filter for dev set
dev_spkrs_list = dev_spkrs.drop(columns='duration')
keys_dev = list(dev_spkrs_list.columns.values)
all_spkrs_index = data_df.set_index(keys_dev).index
dev_spkrs_index = dev_spkrs_list.set_index(keys_dev).index
# Get all the dev rows i.e. speakers in dev speakers
dev_df = data_df[all_spkrs_index.isin(dev_spkrs_index)]

# Filter for test set
test_spkrs_list = test_spkrs.drop(columns='duration')
keys_test = list(test_spkrs_list.columns.values)
all_spkrs_index = data_df.set_index(keys_test).index
test_spkrs_index = test_spkrs_list.set_index(keys_test).index
# Get all the dev rows i.e. speakers in dev speakers
test_df = data_df[all_spkrs_index.isin(test_spkrs_index)]

# ------------------------------------------
#          Saving to csv files
# ------------------------------------------
# Save spkr_id as string so leading zeros are not removed
train_df['spkr_id'] = train_df['spkr_id'].astype('str')
dev_df['spkr_id'] = dev_df['spkr_id'].astype('str')
test_df['spkr_id'] = test_df['spkr_id'].astype('str')
# Save as csv file
train_df.to_csv(data_train_fp, index=False)
dev_df.to_csv(data_dev_fp, index=False)
test_df.to_csv(data_test_fp, index=False)
# Success message
print("SUCCESS: Created train portions in",
      data_train_fp, "and dev portions in", 
      data_dev_fp, "and test portions in",
      data_test_fp)
train_hours = sum(train_df['duration'].tolist())/(60*60)
dev_hours = sum(dev_df['duration'].tolist())/(60*60)
test_hours = sum(test_df['duration'].tolist())/(60*60)
print("Train samples:", len(train_df),
      "| Train hours:", train_hours)
print("Dev samples:", len(dev_df),
      "| Dev hours:", dev_hours)
print("Test samples:", len(test_df),
      "| Test hours:", test_hours)
